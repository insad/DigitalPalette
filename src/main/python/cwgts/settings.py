# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from cguis.setting_dialog import Ui_setting_dialog
from cguis.resource import view_rc
from clibs.argument import Argument
import os


class Settings(QDialog, Ui_setting_dialog):
    """
    Settings dialog for argument setting.
    """

    settings_changed = pyqtSignal(bool)

    def __init__(self, default_settings, resources):
        """
        Init the settings view area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()
        self.setupUi(self)

        # set icon and title.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_256.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Settings")

        # load settings. src\main\resources\base\language
        self.argu = Argument(default_settings, os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette")), os.sep.join((resources, "languages")))

        # init lang cobox values. (part 1)
        for lang_path in self.argu.lang_paths:
            self.st_cobox_21.addItem("")

        # load texts.
        self._func_tr_()

        if self.argu.err:
            QMessageBox.warning(self, self._err_descs[0], self._err_descs[self.argu.err[0]].format(self.argu.err[1]))
            self.argu.save_settings()

        # init button values.
        self.reset_all(self.argu.settings)

        # changed values.
        self._changed = {}

        self.buttonBox.accepted.connect(self.slot_accepted)
        self.buttonBox.rejected.connect(self.slot_rejected)

        btn = self.buttonBox.button(QDialogButtonBox.Apply)
        btn.clicked.connect(self.slot_accepted)

        btn = self.buttonBox.button(QDialogButtonBox.Reset)
        btn.clicked.connect(self.slot_reset)

        # ("h_range", "s_range", "v_range")
        for idx in (0, 1, 2):
            range_from = getattr(self, "st_dp_{}_from".format(idx))
            range_to = getattr(self, "st_dp_{}_to".format(idx))

            range_from.valueChanged.connect(self.slot_change_range(idx))
            range_to.valueChanged.connect(self.slot_change_range(idx))
        
        # hm_rule
        self.st_comb_20.currentIndexChanged.connect(self.slot_change_hm_rule)
        
        # press_move
        self.st_cbox_22.stateChanged.connect(self.slot_change_value(22))

        # graph_types, graph_chls
        for i in range(4):
            gph_tp = getattr(self, "st_cobox_18_{}".format(i))
            chl_tp = getattr(self, "st_cobox_19_{}".format(i))

            gph_tp.currentIndexChanged.connect(self.slot_change_types(18))
            chl_tp.currentIndexChanged.connect(self.slot_change_types(19))
        
        # ("zoom_step", "move_step", "select_dist", "widratio", "radius", "color_radius", "bar_widratio", "tip_radius", "half_sp")
        for idx in (8, 9, 10, 6, 3, 4, 7, 5, 11):
            keyword = getattr(self, "st_p_{}".format(idx))
            keyword.valueChanged.connect(self.slot_change_value(idx))
        
        # ("at_color", "ia_color", "vb_color", "vs_color", "st_color", "it_color")
        for idx in (12, 13, 14, 15, 16, 17):
            color_r = getattr(self, "st_sp_{}_r".format(idx))
            color_g = getattr(self, "st_sp_{}_g".format(idx))
            color_b = getattr(self, "st_sp_{}_b".format(idx))

            color_r.valueChanged.connect(self.slot_change_color(idx))
            color_g.valueChanged.connect(self.slot_change_color(idx))
            color_b.valueChanged.connect(self.slot_change_color(idx))
        
        # "lang"
        self.st_cobox_21.currentIndexChanged.connect(self.slot_change_lang)

    def reset_all(self, settings):
        # ("h_range", "s_range", "v_range")
        for idx in (0, 1, 2):
            range_from = getattr(self, "st_dp_{}_from".format(idx))
            range_to = getattr(self, "st_dp_{}_to".format(idx))
            
            range_from.setValue(settings[idx][0])
            range_to.setValue(settings[idx][1])
        
        # hm_rule
        self.st_comb_20.setCurrentIndex(self.argu.hm_rules.index(settings[20]))
        
        # press_move
        self.st_cbox_22.setChecked(settings[22])

        # graph_types, graph_chls
        for i in range(4):
            gph_tp = getattr(self, "st_cobox_18_{}".format(i))
            chl_tp = getattr(self, "st_cobox_19_{}".format(i))

            gph_tp.setCurrentIndex(settings[18][i])
            chl_tp.setCurrentIndex(settings[19][i])
        
        # ("zoom_step", "move_step", "select_dist", "widratio", "radius", "color_radius", "bar_widratio", "tip_radius", "half_sp")
        for idx in (8, 9, 10, 6, 3, 4, 7, 5, 11):
            keyword = getattr(self, "st_p_{}".format(idx))
            keyword.setValue(settings[idx])
        
        # ("at_color", "ia_color", "vb_color", "vs_color", "st_color", "it_color")
        for idx in (12, 13, 14, 15, 16, 17):
            color_r = getattr(self, "st_sp_{}_r".format(idx))
            color_g = getattr(self, "st_sp_{}_g".format(idx))
            color_b = getattr(self, "st_sp_{}_b".format(idx))
            
            color_r.setValue(settings[idx][0])
            color_g.setValue(settings[idx][1])
            color_b.setValue(settings[idx][2])
        
        # "lang"
        self.st_cobox_21.setCurrentIndex(self.argu.settings[21][0])
    
    def slot_change_range(self, idx):
        def _func_(value):
            range_from = getattr(self, "st_dp_{}_from".format(idx))
            range_to = getattr(self, "st_dp_{}_to".format(idx))

            self._changed[idx] = (range_from.value(), range_to.value())
        return _func_
    
    def slot_change_hm_rule(self, value):
        self._changed[20] = self.argu.hm_rules[value]
    
    def slot_change_types(self, idx):
        def _func_(value):
            tp_list = []
            for i in range(4):
                tp = getattr(self, "st_cobox_{}_{}".format(idx, i))
                tp_list.append(tp.currentIndex())
            self._changed[idx] = tp_list
        return _func_

    def slot_change_color(self, idx):
        def _func_(value):
            color_r = getattr(self, "st_sp_{}_r".format(idx))
            color_g = getattr(self, "st_sp_{}_g".format(idx))
            color_b = getattr(self, "st_sp_{}_b".format(idx))

            self._changed[idx] = (color_r.value(), color_g.value(), color_b.value())
        return _func_

    def slot_change_value(self, idx):
        def _func_(value):
            self._changed[idx] = value
        return _func_
    
    def slot_change_lang(self, value):
        self._changed[21] = (value, "")

    def slot_accepted(self):
        err_lst = self.argu.modify_settings(tuple(zip(self._changed.keys(), self._changed.values())))

        if err_lst:
            QMessageBox.warning(self, self._err_descs[0], self._err_descs[4].format(err_lst))

        self.settings_changed.emit(True)
        self.argu.save_settings()

        self.reset_all(self.argu.settings)
        self._changed = {}

    def slot_rejected(self):
        self.reset_all(self.argu.settings)
        self._changed = {}

    def slot_reset(self):
        self.argu.reset_settings()
        
        self.settings_changed.emit(True)
        self.argu.save_settings()

        self.reset_all(self.argu.settings)
        self._changed = {}

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._err_descs = (
            _translate("Settings", "Error"),
            _translate("Settings", "Values stored in settings file are invalid. (info: {0}) Using default settings instead."),
            _translate("Settings", "Version is not compatible for settings file: {0}. Using default settings instead."),
            _translate("Settings", "Settings file is broken. Using default settings instead."),
            _translate("Settings", "Unable to set these items with values: {0}."),
        )

        self._lang_descs = (
            _translate("Settings", "en"),
            _translate("Settings", "ar"),
            _translate("Settings", "be"),
            _translate("Settings", "bg"),
            _translate("Settings", "ca"),
            _translate("Settings", "cs"),
            _translate("Settings", "da"),
            _translate("Settings", "de"),
            _translate("Settings", "el"),
            _translate("Settings", "es"),
            _translate("Settings", "et"),
            _translate("Settings", "fi"),
            _translate("Settings", "fr"),
            _translate("Settings", "hr"),
            _translate("Settings", "hu"),
            _translate("Settings", "is"),
            _translate("Settings", "it"),
            _translate("Settings", "iw"),
            _translate("Settings", "ja"),
            _translate("Settings", "ko"),
            _translate("Settings", "lt"),
            _translate("Settings", "lv"),
            _translate("Settings", "mk"),
            _translate("Settings", "nl"),
            _translate("Settings", "no"),
            _translate("Settings", "pl"),
            _translate("Settings", "pt"),
            _translate("Settings", "ro"),
            _translate("Settings", "ru"),
            _translate("Settings", "sh"),
            _translate("Settings", "sk"),
            _translate("Settings", "sl"),
            _translate("Settings", "sq"),
            _translate("Settings", "sr"),
            _translate("Settings", "sv"),
            _translate("Settings", "th"),
            _translate("Settings", "tr"),
            _translate("Settings", "uk"),
            _translate("Settings", "zh"),
            _translate("Settings", "default"),
        )

        # init lang cobox values. (part 2)
        for idx in range(len(self.argu.lang_paths)):
            lang_path = self.argu.lang_paths[idx]
            abbr_name = os.path.basename(lang_path[1]).split(".")[0]
            self.st_cobox_21.setItemText(idx, self._lang_descs[lang_path[0]] + " ({})".format(abbr_name))