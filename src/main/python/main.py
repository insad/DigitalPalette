# -*- coding: utf-8 -*-

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QHBoxLayout, QWidget, QMessageBox
from cguis.main_window import Ui_MainWindow
from cguis.scroll_result_form import Ui_scroll_result
from cwgts.wheel import Wheel
from cwgts.square import Square
from clibs.color import Color
from clibs import info as dpinfo
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
import sys


__info__ = """
    DigitalPalette Info

    --------------
    Version: {}
    Author: Liu Jia
    Update: {}
    Website: {}
    --------------

    DigitalPalette is distributed under GPL v3 license.
""".format(dpinfo.current_version(), dpinfo.update_date(), dpinfo.website())


class DigitalPalette(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("DigitalPalette {}".format(dpinfo.current_version()))
        self.setWindowIcon(QIcon("./src/main/icons/base/128.png"))

        self._setting_env = {"h_range": (0.0, 360.0),     # H range for initial random HSV color set. For create.py. By wheel.py.
                             "s_range": (0.8, 1.0),       # S range for initial random HSV color set. For create.py. By wheel.py.
                             "v_range": (0.8, 1.0),       # V range for initial random HSV color set. For create.py. By wheel.py.
                             "radius": 0.8,               # Color wheel radius (ratio) compared with work space width. For wheel.py. By wheel.py.
                             "color_radius": 0.05,        # Color tag radius (ratio)  compared with work space width. For wheel.py. By wheel.py.
                             "bar_widratio": 0.65,        # V value bar width / height ratio compared with work space. For wheel.py. By wheel.py.
                             "hm_rule": "analogous",      # Initial harmony rule. For create.py. By wheel.py.
                             "press_move": True,          # Press anywhere in wheel will move activated color tag to the selected color. For wheel.py. By wheel.py.
                             "at_color": (0, 0, 0),       # activated color for color tag in wheel and square. For wheel.py and square.py. By wheel.py and square.py.
                             "ia_color": (200, 200, 200), # inactivated color for color tags in wheel and squares. For wheel.py and square.py. By wheel.py and square.py.
                             "vb_color": (230, 230, 230), # V value bar color. For wheel.py. By wheel.py.
                             "widratio": 0.9,             # Color square width / height ratio compared with cube size. For square.py. By square.py.
                             }

        self._setup_default_env()
        self._setup_wheel()
        self._setup_scroll_result()
        self._setup_operation()
        self._setup_msg()

    def _setup_msg(self):
        self.actionAbout.triggered.connect(self._show_info_)
        self.actionUpdate.triggered.connect(lambda x: QDesktopServices.openUrl(QUrl(dpinfo.website())))

    def _setup_default_env(self):
        # setup default harmony rule.
        hm_rules = getattr(self, "rbtn_{}".format(self._setting_env["hm_rule"]))
        hm_rules.setChecked(True)

    def _setup_wheel(self):
        grid_layout = QGridLayout(self.workspace)
        grid_layout.setContentsMargins(2, 2, 2, 2)
        self._cwgt_wheel = Wheel(setting=self._setting_env)
        grid_layout.addWidget(self._cwgt_wheel)
        self.workspace.setLayout(grid_layout)

        for hm_rule in ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom"):
            rbtn_hm_rule = getattr(self, "rbtn_{}".format(hm_rule))
            rbtn_hm_rule.clicked.connect(self._cwgt_wheel.slot_modify_hm_rule(hm_rule.lower()))

        self._cwgt_wheel.selected_hm_rule.connect(self._func_set_hm_rule_buttons)
        self.pbtn_Create.clicked.connect(self._cwgt_wheel.slot_recreate)

    def _setup_scroll_result(self):
        scroll_result = Ui_scroll_result()
        scroll_result.setupUi(self.result)

        self._cube_squares = []

        for idx in range(5):
            # create square objects.
            cube_color = getattr(scroll_result, "color_{}".format(idx))
            cube_grid_layout = QGridLayout(cube_color)
            cube_grid_layout.setContentsMargins(0, 0, 0, 0)
            cube_square = Square(setting=self._setting_env)
            cube_grid_layout.addWidget(cube_square)
            cube_color.setLayout(cube_grid_layout)

            self._cube_squares.append(cube_square)

            # init cube square colors by color set of wheel.
            cube_square.slot_change_color(self._cwgt_wheel.color_set[idx].hsv)

            # set rgb gbox visibility.
            rgb_gbox = getattr(scroll_result, "gbox_RGB_{}".format(idx))
            if self.cbox_RGB.isChecked():
                rgb_gbox.setVisible(True)
            else:
                rgb_gbox.setVisible(False)
            self.cbox_RGB.stateChanged.connect(rgb_gbox.setVisible)

            # set connections between rgb sliders and rgb spin boxes.
            for ctype in ("r", "g", "b"):
                hs_RGB = getattr(scroll_result, "hs_RGB_{}_{}".format(ctype, idx))
                hs_RGB.valueChanged.connect(self._func_RGB_hs_to_sp_(scroll_result, "sp_RGB_{}_{}".format(ctype, idx)))

                sp_RGB = getattr(scroll_result, "sp_RGB_{}_{}".format(ctype, idx))
                sp_RGB.valueChanged.connect(self._func_RGB_sp_to_hs_(scroll_result, "hs_RGB_{}_{}".format(ctype, idx)))

                # set connections from rgb spin boxes to cube squares.
                sp_RGB.valueChanged.connect(cube_square.slot_change_rgb(ctype))

            # set hsv gbox visibility.
            hsv_gbox = getattr(scroll_result, "gbox_HSV_{}".format(idx))
            if self.cbox_HSV.isChecked():
                hsv_gbox.setVisible(True)
            else:
                hsv_gbox.setVisible(False)
            self.cbox_HSV.stateChanged.connect(hsv_gbox.setVisible)

            # set connections between hsv sliders and hsv double spin boxes.
            for ctype in ("h", "s", "v"):
                hs_HSV = getattr(scroll_result, "hs_HSV_{}_{}".format(ctype, idx))
                hs_HSV.valueChanged.connect(self._func_HSV_hs_to_dp_(scroll_result, "dp_HSV_{}_{}".format(ctype, idx)))

                dp_HSV = getattr(scroll_result, "dp_HSV_{}_{}".format(ctype, idx))
                dp_HSV.valueChanged.connect(self._func_HSV_dp_to_hs_(scroll_result, "hs_HSV_{}_{}".format(ctype, idx)))

                # set connections from hsv double spin boxes to cube squares.
                dp_HSV.valueChanged.connect(cube_square.slot_change_hsv(ctype))

            # set connections from cube squares to rgb spin boxes.
            for ctype in ("r", "g", "b"):
                cube_selected = getattr(cube_square, "selected_{}".format(ctype))
                cube_selected.connect(self._func_set_value_(scroll_result, "sp_RGB_{}_{}".format(ctype, idx)))

            # set connections from cube squares to hsv double spin boxes.
            for ctype in ("h", "s", "v"):
                cube_selected = getattr(cube_square, "selected_{}".format(ctype))
                cube_selected.connect(self._func_set_value_(scroll_result, "dp_HSV_{}_{}".format(ctype, idx)))

            # set connection from cube square to corresponding wheel color.
            cube_square.selected_hsv.connect(self._cwgt_wheel.slot_modify_color(idx))

            # set connection from wheel color to corresponding cube square.
            wheel_selected_color = getattr(self._cwgt_wheel, "selected_color_{}".format(idx))
            wheel_selected_color.connect(cube_square.slot_change_color)

            # init cube square state. default 0 is activated.
            if idx == 0:
                cube_square.slot_wheel_change_active_state(True)
            else:
                cube_square.slot_wheel_change_active_state(False)

            # set connections bwtween wheel activated color and cube square states.
            selected_acitve = getattr(self._cwgt_wheel, "selected_acitve_{}".format(idx))
            selected_acitve.connect(cube_square.slot_wheel_change_active_state)
            cube_square.selected_active.connect(self._cwgt_wheel.slot_modify_activate_index(idx))

            # set connections between cube square and hex code line edits.
            cube_ledit = getattr(scroll_result, "le_hex_{}".format(idx))
            cube_square.selected_hex.connect(cube_ledit.setText)
            cube_ledit.textChanged.connect(cube_square.slot_change_hex_code)

    def _setup_operation(self):
        self.pbtn_Import.clicked.connect(self._cwgt_wheel.slot_import)
        self.pbtn_Export.clicked.connect(self._cwgt_wheel.slot_export)


    # ===== ===== ===== inner functions and decorators below ===== ===== =====

    # set spin box's value by slider's value in result area.
    def _func_RGB_hs_to_sp_(self, obj, name):
        def _func_(value):
            sp = getattr(obj, name)
            sp.setValue(int(value))
        return _func_

    def _func_HSV_hs_to_dp_(self, obj, name):
        def _func_(value):
            sp = getattr(obj, name)
            sp.setValue(float(value / 1E3))
        return _func_

    # set slider's value by spin box's value.
    def _func_RGB_sp_to_hs_(self, obj, name):
        def _func_(value):
            hs = getattr(obj, name)
            hs.setValue(int(value))
        return _func_

    def _func_HSV_dp_to_hs_(self, obj, name):
        def _func_(value):
            hs = getattr(obj, name)
            hs.setValue(int(value * 1E3))
        return _func_

    # set object's value generally.
    def _func_set_value_(self, obj, name):
        def _func_(value):
            sp = getattr(obj, name)
            sp.setValue(value)
        return _func_

    # set hm rule buttons.
    def _func_set_hm_rule_buttons(self, hm_rule):
        for pr_hm_rule in ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom"):
            if pr_hm_rule.lower() == hm_rule:
                rbtn_hm_rule = getattr(self, "rbtn_{}".format(pr_hm_rule))
                rbtn_hm_rule.click()

    # show DigitalPalette information.
    def _show_info_(self):
        QMessageBox.information(self, "About", __info__)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    DP = DigitalPalette()
    DP.show()
    sys.exit(app.exec())
