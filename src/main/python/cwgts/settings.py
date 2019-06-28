# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from cguis.setting_dialog import Ui_setting_dialog
from PyQt5.QtCore import pyqtSignal


class Settings(QDialog, Ui_setting_dialog):
    """
    Settings dialog for argument setting.
    """

    changed_setti = pyqtSignal(dict)

    def __init__(self, default_setting, setting):
        """
        Init the settings view area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()
        self.setupUi(self)

        self._changed = {}
        self._hm_rules = ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom")

        self.buttonBox.accepted.connect(self.slot_accepted)
        self.buttonBox.rejected.connect(self.slot_rejected)

        btn = self.buttonBox.button(QDialogButtonBox.Apply)
        btn.clicked.connect(self.slot_accepted)

        btn = self.buttonBox.button(QDialogButtonBox.Reset)
        btn.clicked.connect(self.slot_reseting(default_setting))

        self.reset_all(setting)

        for name in ("h_range", "s_range", "v_range"):
            range_from = getattr(self, "st_dp_{}_from".format(name))
            range_to = getattr(self, "st_dp_{}_to".format(name))

            range_from.valueChanged.connect(self.slot_change_range(name))
            range_to.valueChanged.connect(self.slot_change_range(name))
        
        self.st_comb_hm_rule.currentIndexChanged.connect(self.slot_change_hm_rule)
        
        self.st_cbox_press_move.stateChanged.connect(self.slot_change_value("press_move"))

        for i in range(4):
            gph_tp = getattr(self, "st_cobox_graph_types_{}".format(i))
            chl_tp = getattr(self, "st_cobox_graph_chls_{}".format(i))

            gph_tp.currentIndexChanged.connect(self.slot_change_types("graph_types"))
            chl_tp.currentIndexChanged.connect(self.slot_change_types("graph_chls"))
        
        for name in ("zoom_step", "move_step", "select_dist", "widratio", "radius", "color_radius", "bar_widratio", "tip_radius", "half_sp"):
            keyword = getattr(self, "st_p_{}".format(name))
            keyword.valueChanged.connect(self.slot_change_value(name))
        
        for name in ("at_color", "ia_color", "vb_color", "vs_color", "st_color", "it_color"):
            color_r = getattr(self, "st_sp_{}_r".format(name))
            color_g = getattr(self, "st_sp_{}_g".format(name))
            color_b = getattr(self, "st_sp_{}_b".format(name))

            color_r.valueChanged.connect(self.slot_change_color(name))
            color_g.valueChanged.connect(self.slot_change_color(name))
            color_b.valueChanged.connect(self.slot_change_color(name))
        
        for name in ("en", "zh_CN"):
            rbtn_lang = getattr(self, "st_rbtn_{}".format(name))
            rbtn_lang.clicked.connect(self.slot_change_lang(name))

    def reset_all(self, setting):
        for name in ("h_range", "s_range", "v_range"):
            range_from = getattr(self, "st_dp_{}_from".format(name))
            range_to = getattr(self, "st_dp_{}_to".format(name))
            
            range_from.setValue(setting[name][0])
            range_to.setValue(setting[name][1])
        
        self.st_comb_hm_rule.setCurrentIndex(self._hm_rules.index(setting["hm_rule"]))
        
        self.st_cbox_press_move.setChecked(setting["press_move"])

        for i in range(4):
            gph_tp = getattr(self, "st_cobox_graph_types_{}".format(i))
            chl_tp = getattr(self, "st_cobox_graph_chls_{}".format(i))

            gph_tp.setCurrentIndex(setting["graph_types"][i])
            chl_tp.setCurrentIndex(setting["graph_chls"][i])
        
        for name in ("zoom_step", "move_step", "select_dist", "widratio", "radius", "color_radius", "bar_widratio", "tip_radius", "half_sp"):
            keyword = getattr(self, "st_p_{}".format(name))
            keyword.setValue(setting[name])
        
        for name in ("at_color", "ia_color", "vb_color", "vs_color", "st_color", "it_color"):
            color_r = getattr(self, "st_sp_{}_r".format(name))
            color_g = getattr(self, "st_sp_{}_g".format(name))
            color_b = getattr(self, "st_sp_{}_b".format(name))
            
            color_r.setValue(setting[name][0])
            color_g.setValue(setting[name][1])
            color_b.setValue(setting[name][2])
        
        st_rbtn_lang = getattr(self, "st_rbtn_{}".format(setting["lang"]))
        st_rbtn_lang.click()
    
    def slot_change_range(self, name):
        def _func_(value):
            range_from = getattr(self, "st_dp_{}_from".format(name))
            range_to = getattr(self, "st_dp_{}_to".format(name))

            self._changed[name] = (range_from.value(), range_to.value())
        return _func_
    
    def slot_change_hm_rule(self, value):
        self._changed["hm_rule"] = self._hm_rules[value]
    
    def slot_change_types(self, name):
        def _func_(value):
            tp_list = []
            for i in range(4):
                tp = getattr(self, "st_cobox_{}_{}".format(name, i))
                tp_list.append(tp.currentIndex())
            self._changed[name] = tp_list
        return _func_

    def slot_change_color(self, name):
        def _func_(value):
            color_r = getattr(self, "st_sp_{}_r".format(name))
            color_g = getattr(self, "st_sp_{}_g".format(name))
            color_b = getattr(self, "st_sp_{}_b".format(name))

            self._changed[name] = (color_r.value(), color_g.value(), color_b.value())
        return _func_

    def slot_change_value(self, name):
        def _func_(value):
            self._changed[name] = value
        return _func_
    
    def slot_change_lang(self, name):
        def _func_(value):
            self._changed["lang"] = name
        return _func_

    def slot_accepted(self):
        self.changed_setti.emit(self._changed)
        self._changed = {}
    
    def slot_rejected(self):
        self._changed = {}
    
    def slot_reseting(self, default_setting):
        def _func_():
            self.reset_all(default_setting)
        return _func_
