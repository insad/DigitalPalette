# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in 
the hope that it will be useful, but WITHOUT ANY WARRANTY. 
You can redistribute it and/or modify it under the terms of 
the GNU General Public License as published by the Free 
Software Foundation. See the GNU General Public License 
for more details.
"""

from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QMessageBox
from cguis.main_window import Ui_MainWindow
from cguis.resource import view_rc
from cwgts.wheel import Wheel
from cwgts.graph import Graph
from cwgts.result import Result
from cwgts.settings import Settings
from clibs import info as dpinfo
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtCore import QUrl, QTranslator, QCoreApplication
import sys
import os


class DigitalPalette(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("DigitalPalette {}".format(dpinfo.current_version()))
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_256.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        # init settings.
        default_settings = (
            (0.0, 360.0),     # 0  # "h_range":      # H range for initial random HSV color set.
            (0.68, 1.0),      # 1  # "s_range":      # S range for initial random HSV color set.
            (0.68, 1.0),      # 2  # "v_range":      # V range for initial random HSV color set.
            0.8,              # 3  # "radius":       # Color wheel radius (ratio) compared with work space width.
            0.05,             # 4  # "color_radius": # Color tag radius (ratio)  compared with work space width.
            0.1,              # 5  # "tip_radius":   # Circle tip radius in graph view.
            0.9,              # 6  # "widratio":     # Color square width / height ratio compared with cube size.
            0.8,              # 7  # "bar_widratio": # V value bar height ratio compared with work space.
            1.3,              # 8  # "zoom_step":    # zoom ratio for each step.
            5,                # 9  # "move_step":    # graph move lengtho for each step.
            10,               # 10 # "select_dist":  # minimal selecting distance.
            5,                # 11 # "half_sp":      # Half of spacing between two views in graph.
            (0,   0,   0  ),  # 12 # "at_color":     # activated color for color tag in wheel and square. For wheel.py and square.py.
            (200, 200, 200),  # 13 # "ia_color":     # inactivated color for color tags in wheel and squares. For wheel.py and square.py.
            (230, 230, 230),  # 14 # "vb_color":     # V value bar edge color.
            (100, 100, 100),  # 15 # "vs_color":     # View window tip color.
            (100, 100, 100),  # 16 # "st_color":     # select circle color in graph views.
            (200, 200, 200),  # 17 # "it_color":     # referenced select circle color in graph views.
            [0, 7, 7, 7],     # 18 # "graph_types":  # Graph types corresponding to temporary files.
            [0, 1, 2, 3],     # 19 #  "graph_chls":  # Graph channels corresponding to temporary files.
            "analogous",      # 20 # "hm_rule":      # Initial harmony rule.
            "en",             # 21 # "lang":         # default language.
            True,             # 22 # "press_move":   # Press anywhere in wheel will move activated color tag to the selected color.
        )

        self._settings = Settings(default_settings)
        self._settings.settings_changed.connect(self._func_reload_settings_)

        # init translator.
        self._tr = QTranslator()
        self._app = QApplication.instance()

        self._setup_wheel()
        self._setup_scroll_result()
        self._setup_interface()

    def _setup_wheel(self):
        """
        Setup work area (wheel or graph).
        """

        work_grid_layout = QGridLayout(self.workspace)
        work_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._cwgt_wheel = Wheel(self._settings.argu.settings)
        work_grid_layout.addWidget(self._cwgt_wheel)

        self._cwgt_graph = Graph(self._settings.argu.settings)
        self._cwgt_graph.hide()
        work_grid_layout.addWidget(self._cwgt_graph)

        self.workspace.setLayout(work_grid_layout)

        # set connections between button hm rule and wheel hm rule.
        for hm_rule in ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom"):
            rbtn_hm_rule = getattr(self, "rbtn_{}".format(hm_rule))
            rbtn_hm_rule.clicked.connect(self._cwgt_wheel.slot_modify_hm_rule(hm_rule))
            rbtn_hm_rule.clicked.connect(self._cwgt_graph.slot_set_hm_rule(hm_rule))

        self._cwgt_wheel.selected_hm_rule.connect(self._func_set_hm_rule_buttons) # for loading json files.

    def _setup_scroll_result(self):
        """
        Setup scroll result area.
        """

        rst_grid_layout = QGridLayout(self.result)
        rst_grid_layout.setContentsMargins(2, 2, 2, 2)

        self._cwgt_result = Result(self._settings.argu.settings)
        rst_grid_layout.addWidget(self._cwgt_result)
        self.result.setLayout(rst_grid_layout)

        self._cwgt_result.slot_change_rgb_visibility(self.cbox_RGB.isChecked())
        self._cwgt_result.slot_change_hsv_visibility(self.cbox_HSV.isChecked())
        self.cbox_RGB.stateChanged.connect(self._cwgt_result.slot_change_rgb_visibility)
        self.cbox_HSV.stateChanged.connect(self._cwgt_result.slot_change_hsv_visibility)

        for idx in range(5):
            cube_square = self._cwgt_result.cube_squares[idx]

            # init cube square colors by color set of wheel.
            cube_square.slot_change_color(self._cwgt_wheel.color_set[idx].hsv)

            # set connection from cube square to corresponding wheel color.
            cube_square.selected_hsv.connect(self._cwgt_wheel.slot_modify_color(idx))

            # set connection from wheel color to corresponding cube square.
            wheel_selected_color = getattr(self._cwgt_wheel, "selected_color_{}".format(idx))
            wheel_selected_color.connect(cube_square.slot_change_color)

            # set connection from graph view color to corresponding cube square.
            graph_selected_tr_color = getattr(self._cwgt_graph, "selected_tr_color_{}".format(idx))
            graph_selected_tr_color.connect(cube_square.slot_change_graph_color)

            # set connections bwtween wheel activated color and cube square states.
            selected_acitve = getattr(self._cwgt_wheel, "selected_acitve_{}".format(idx))
            selected_acitve.connect(cube_square.slot_wheel_change_active_state)
            cube_square.selected_active.connect(self._cwgt_wheel.slot_modify_activate_index(idx))

    def _setup_interface(self):
        """
        Setup operation. At end.
        """

        hm_rules = getattr(self, "rbtn_{}".format(self._settings.argu.settings[20]))
        hm_rules.setChecked(True)

        self.pbtn_Import.clicked.connect(self._cwgt_wheel.slot_import)
        self.pbtn_Export.clicked.connect(self._cwgt_wheel.slot_export)

        self.actionAbout.triggered.connect(self._show_info_)
        self.actionUpdate.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(dpinfo.website())))

        self.pbtn_Create.clicked.connect(self._func_resetup_wheel_)
        self.pbtn_Extract.clicked.connect(self._func_resetup_graph_)

        self.actionSettings.triggered.connect(self._settings.show)

        self._ori_lang = self._settings.argu.settings[21]

        self._func_reload_local_lang_()


    # ===== ===== ===== inner functions and decorators below ===== ===== =====

    # set hm rule buttons.
    def _func_set_hm_rule_buttons(self, hm_rule):
        for pr_hm_rule in self._settings.argu.hm_rules:
            if pr_hm_rule.lower() == hm_rule:
                rbtn_hm_rule = getattr(self, "rbtn_{}".format(pr_hm_rule))
                rbtn_hm_rule.click()

    # show DigitalPalette information.
    def _show_info_(self):
        QMessageBox.information(self, self._info_descs[0], "\n".join(self._info_descs[1:]).format(dpinfo.current_version(), "Liu Jia", dpinfo.update_date(), dpinfo.website()))

    def _func_resetup_wheel_(self):
        if self._cwgt_wheel.isVisible():
            self._cwgt_wheel.slot_recreate()
        else:
            self._cwgt_wheel.show()
            self._cwgt_graph.hide()
            for hm_rule in self._settings.argu.hm_rules[:-1]:
                rbtn_hm_rule = getattr(self, "rbtn_{}".format(hm_rule))
                rbtn_hm_rule.show()
        
        for idx in range(5):
            self._cwgt_result.cube_squares[idx].slot_active_on(True)

    def _func_resetup_graph_(self):
        if self._cwgt_graph.isVisible():
            self._cwgt_graph.slot_open_graph()
        else:
            self._cwgt_wheel.hide()
            self._cwgt_graph.show()
            for hm_rule in self._settings.argu.hm_rules[:-1]:
                rbtn_hm_rule = getattr(self, "rbtn_{}".format(hm_rule))
                rbtn_hm_rule.hide()
            
            self._cwgt_graph.slot_update()

        for idx in range(5):
            self._cwgt_result.cube_squares[idx].slot_active_on(False)

    def _func_reload_settings_(self, value):
        """
        Reload local settings by user settings.
        """

        self._cwgt_wheel.reload_settings(self._settings.argu.settings)
        self._cwgt_wheel.update()

        self._cwgt_graph.reload_settings(self._settings.argu.settings)
        self._cwgt_graph.reload_view_settings()
        self._cwgt_graph.update()

        for cube_square in self._cwgt_result.cube_squares:
            cube_square.reload_settings(self._settings.argu.settings)
            cube_square.update()
        
        """
        if self._env.settings["lang"] != self._lang_path.split(os.sep)[-1].split(".")[0]:
            self._func_reload_local_lang_()
        """
        self.update()


    def _func_reload_local_lang_(self):
        pass
        """"
        if self._settings.argu.settings[21] != self._ori_lang:
            lang_pkgs = os.listdir(os.sep.join((".", "language")
        self._lang_path = os.sep.join((".", "language", self._settings.argu.settings[21] + ".qm"))
        if os.path.isfile(self._lang_path):
            self._tr.load(self._lang_path)
            self._app.installTranslator(self._tr)
            self.retranslateUi(self)
            self._func_tr_()
            self._cwgt_wheel._func_tr_()
            self._cwgt_graph._func_tr_()
        """
        
    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._info_descs = (_translate("DigitalPalette", "About"),
                            _translate("DigitalPalette", "DigitalPalette Info"),
                            _translate("DigitalPalette", "----- ----- ----- -----"),
                            _translate("DigitalPalette", "Version: {0}"),
                            _translate("DigitalPalette", "Author: {1}"),
                            _translate("DigitalPalette", "Update: {2}"),
                            _translate("DigitalPalette", "Github: {3}"),
                            _translate("DigitalPalette", "----- ----- ----- -----"),
                            _translate("DigitalPalette", "DigitalPalette is a free software, which is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License for more details."),)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    DP = DigitalPalette()
    DP.show()
    sys.exit(app.exec())
