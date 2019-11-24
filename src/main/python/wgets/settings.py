# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon, QPixmap
from cguis.design.settings_dialog import Ui_SettingsDialog
from cguis.resource import view_rc
import os


class Settings(QDialog, Ui_SettingsDialog):
    """
    Settings object based on QWidget. Init a settings in settings.
    """

    ps_rule_changed = pyqtSignal(bool)
    ps_lang_changed = pyqtSignal(bool)
    ps_settings_changed = pyqtSignal(bool)

    def __init__(self, args):
        """
        Init rule.
        """

        super().__init__()
        self.setupUi(self)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_256.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)
        self.setWindowTitle("Settings")

        # init comb boxes.
        for lang in self._args.usr_langs:
            self.lang_comb.addItem("")

        for method in self._args.global_hm_rules:
            self.hm_rule_comb.addItem("")

        for overfl in self._args.global_overflows:
            self.overflow_comb.addItem("")

        # init buttons.
        btn = self.buttonBox.button(QDialogButtonBox.Ok)
        btn.setText(self._btn_descs[0])
        btn.clicked.connect(self.application)

        btn = self.buttonBox.button(QDialogButtonBox.Cancel)
        btn.setText(self._btn_descs[1])
        btn.clicked.connect(self.close)

        btn = self.buttonBox.button(QDialogButtonBox.Apply)
        btn.setText(self._btn_descs[2])
        btn.clicked.connect(self.update_values)

        btn = self.buttonBox.button(QDialogButtonBox.Reset)
        btn.setText(self._btn_descs[3])
        btn.clicked.connect(self.reset_values)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def initialize(self):
        """
        Initialize values of boxes in settings dialog by self._args.
        """

        self.usr_color_ledit.setText(self._args.usr_color)
        self.usr_image_ledit.setText(self._args.usr_image)

        self.store_loc_cbox.setChecked(self._args.store_loc)

        self.hm_rule_comb.setCurrentIndex(self._args.global_hm_rules.index(self._args.hm_rule))
        self.overflow_comb.setCurrentIndex(self._args.global_overflows.index(self._args.overflow))

        self.lang_comb.setCurrentIndex([x[1] for x in self._args.usr_langs].index(self._args.lang))

        self.press_move_cbox.setChecked(self._args.press_move)
        self.show_hsv_cbox.setChecked(self._args.show_hsv)
        self.show_rgb_cbox.setChecked(self._args.show_rgb)

        self.h_range_0_dp.setValue(self._args.h_range[0])
        self.h_range_1_dp.setValue(self._args.h_range[1])
        self.s_range_0_dp.setValue(self._args.s_range[0])
        self.s_range_1_dp.setValue(self._args.s_range[1])
        self.v_range_0_dp.setValue(self._args.v_range[0])
        self.v_range_1_dp.setValue(self._args.v_range[1])

        self.wheel_ratio_dp.setValue(self._args.wheel_ratio)
        self.volum_ratio_dp.setValue(self._args.volum_ratio)
        self.cubic_ratio_dp.setValue(self._args.cubic_ratio)

        self.s_tag_radius_dp.setValue(self._args.s_tag_radius)
        self.v_tag_radius_dp.setValue(self._args.v_tag_radius)

        self.zoom_step_dp.setValue(self._args.zoom_step)
        self.move_step_dp.setValue(self._args.move_step)

        self.circle_dist_sp.setValue(self._args.circle_dist)

        self.positive_wid_sp.setValue(self._args.positive_wid)
        self.negative_wid_sp.setValue(self._args.negative_wid)
        self.wheel_ed_wid_sp.setValue(self._args.wheel_ed_wid)

        self.positive_color_0_dp.setValue(self._args.positive_color[0])
        self.positive_color_1_dp.setValue(self._args.positive_color[1])
        self.positive_color_2_dp.setValue(self._args.positive_color[2])
        self.negative_color_0_dp.setValue(self._args.negative_color[0])
        self.negative_color_1_dp.setValue(self._args.negative_color[1])
        self.negative_color_2_dp.setValue(self._args.negative_color[2])
        self.wheel_ed_color_0_dp.setValue(self._args.wheel_ed_color[0])
        self.wheel_ed_color_1_dp.setValue(self._args.wheel_ed_color[1])
        self.wheel_ed_color_2_dp.setValue(self._args.wheel_ed_color[2])

    def application(self):
        """
        Modify self._args by values of boxes in settings dialog.
        """

        self._args.modify_settings("usr_color", self.usr_color_ledit.text())
        self._args.modify_settings("usr_image", self.usr_image_ledit.text())

        self._args.modify_settings("store_loc", self.store_loc_cbox.isChecked())

        hm_rule = self._args.hm_rule
        self._args.modify_settings("hm_rule", self._args.global_hm_rules[self.hm_rule_comb.currentIndex()])

        if self._args.hm_rule != hm_rule:
            self.ps_rule_changed.emit(True)

        self._args.modify_settings("overflow", self._args.global_overflows[self.overflow_comb.currentIndex()])

        lang = self._args.lang
        self._args.modify_settings("lang", self._args.usr_langs[self.lang_comb.currentIndex()][1])

        if self._args.lang != lang:
            self.ps_lang_changed.emit(True)

        self._args.modify_settings("press_move", self.press_move_cbox.isChecked())
        self._args.modify_settings("show_hsv", self.show_hsv_cbox.isChecked())
        self._args.modify_settings("show_rgb", self.show_rgb_cbox.isChecked())

        self._args.modify_settings("h_range", (self.h_range_0_dp.value(), self.h_range_1_dp.value()))
        self._args.modify_settings("s_range", (self.s_range_0_dp.value(), self.s_range_1_dp.value()))
        self._args.modify_settings("v_range", (self.v_range_0_dp.value(), self.v_range_1_dp.value()))

        self._args.modify_settings("wheel_ratio", self.wheel_ratio_dp.value())
        self._args.modify_settings("volum_ratio", self.volum_ratio_dp.value())
        self._args.modify_settings("cubic_ratio", self.cubic_ratio_dp.value())

        self._args.modify_settings("s_tag_radius", self.s_tag_radius_dp.value())
        self._args.modify_settings("v_tag_radius", self.v_tag_radius_dp.value())

        self._args.modify_settings("zoom_step", self.zoom_step_dp.value())
        self._args.modify_settings("move_step", self.move_step_dp.value())

        self._args.modify_settings("circle_dist", self.circle_dist_sp.value())

        self._args.modify_settings("positive_wid", self.positive_wid_sp.value())
        self._args.modify_settings("negative_wid", self.negative_wid_sp.value())
        self._args.modify_settings("wheel_ed_wid", self.wheel_ed_wid_sp.value())

        self._args.modify_settings("positive_color", (self.positive_color_0_dp.value(), self.positive_color_1_dp.value(), self.positive_color_2_dp.value()))
        self._args.modify_settings("negative_color", (self.negative_color_0_dp.value(), self.negative_color_1_dp.value(), self.negative_color_2_dp.value()))
        self._args.modify_settings("wheel_ed_color", (self.wheel_ed_color_0_dp.value(), self.wheel_ed_color_1_dp.value(), self.wheel_ed_color_2_dp.value()))

        self.ps_settings_changed.emit(True)

    def showup(self):
        """
        Initialize and show.
        """

        self.initialize()
        self.show()

    def update_values(self):
        """
        For button apply.
        """

        self.application()
        self.initialize()

    def reset_values(self):
        """
        For button reset.
        """

        hm_rule = self._args.hm_rule
        lang = self._args.lang

        self._args.init_settings()
        self.initialize()

        if self._args.hm_rule != hm_rule:
            self.ps_rule_changed.emit(True)

        if self._args.lang != lang:
            self.ps_lang_changed.emit(True)

        self.ps_settings_changed.emit(True)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        for idx in range(len(self._args.usr_langs)):
            lang = self._args.usr_langs[idx]
            self.lang_comb.setItemText(idx, "{} ({})".format(self._lang_descs[lang[0]], lang[1].split(".")[0]))

        for idx in range(len(self._args.global_hm_rules)):
            self.hm_rule_comb.setItemText(idx, self._rule_descs[idx])

        for idx in range(len(self._args.global_overflows)):
            self.overflow_comb.setItemText(idx, self._overflow_descs[idx])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._btn_descs = (
            _translate("Settings", "OK"),
            _translate("Settings", "Cancel"),
            _translate("Settings", "Apply"),
            _translate("Settings", "Reset"),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )

        self._overflow_descs = (
            _translate("Rule", "Cutoff"),
            _translate("Rule", "Return"),
            _translate("Rule", "Repeat"),
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