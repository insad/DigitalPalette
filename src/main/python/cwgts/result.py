# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
from cguis.scroll_result_form import Ui_scroll_result
from cwgts.square import Square


class Result(QWidget, Ui_scroll_result):
    """
    Result area containing five color squares and slides.
    """

    def __init__(self, settings):
        """
        Init the result area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()
        self.setupUi(self)

        self.cube_squares = []

        for idx in range(5):
            # create square objects.
            cube_color = getattr(self, "color_{}".format(idx))
            cube_grid_layout = QGridLayout(cube_color)
            cube_grid_layout.setContentsMargins(0, 0, 0, 0)
            cube_square = Square(settings)
            cube_grid_layout.addWidget(cube_square)
            cube_color.setLayout(cube_grid_layout)

            self.cube_squares.append(cube_square)

            # set connections between rgb sliders and rgb spin boxes.
            for ctype in ("r", "g", "b"):
                hs_RGB = getattr(self, "hs_RGB_{}_{}".format(ctype, idx))
                hs_RGB.valueChanged.connect(self._func_RGB_hs_to_sp_(self, "sp_RGB_{}_{}".format(ctype, idx)))

                sp_RGB = getattr(self, "sp_RGB_{}_{}".format(ctype, idx))
                sp_RGB.valueChanged.connect(self._func_RGB_sp_to_hs_(self, "hs_RGB_{}_{}".format(ctype, idx)))

                # set connections from rgb spin boxes to cube squares.
                sp_RGB.valueChanged.connect(cube_square.slot_change_rgb(ctype))

            # set connections between hsv sliders and hsv double spin boxes.
            for ctype in ("h", "s", "v"):
                hs_HSV = getattr(self, "hs_HSV_{}_{}".format(ctype, idx))
                hs_HSV.valueChanged.connect(self._func_HSV_hs_to_dp_(self, "dp_HSV_{}_{}".format(ctype, idx)))

                dp_HSV = getattr(self, "dp_HSV_{}_{}".format(ctype, idx))
                dp_HSV.valueChanged.connect(self._func_HSV_dp_to_hs_(self, "hs_HSV_{}_{}".format(ctype, idx)))

                # set connections from hsv double spin boxes to cube squares.
                dp_HSV.valueChanged.connect(cube_square.slot_change_hsv(ctype))

            # set connections from cube squares to rgb spin boxes.
            for ctype in ("r", "g", "b"):
                cube_selected = getattr(cube_square, "selected_{}".format(ctype))
                cube_selected.connect(self._func_set_value_(self, "sp_RGB_{}_{}".format(ctype, idx)))

            # set connections from cube squares to hsv double spin boxes.
            for ctype in ("h", "s", "v"):
                cube_selected = getattr(cube_square, "selected_{}".format(ctype))
                cube_selected.connect(self._func_set_value_(self, "dp_HSV_{}_{}".format(ctype, idx)))

            # init cube square state. default 0 is activated.
            if idx == 0:
                cube_square.slot_wheel_change_active_state(True)
            else:
                cube_square.slot_wheel_change_active_state(False)

            # set connections between cube square and hex code line edits.
            cube_ledit = getattr(self, "le_hex_{}".format(idx))
            cube_square.selected_hex.connect(cube_ledit.setText)
            cube_ledit.textChanged.connect(cube_square.slot_change_hex_code)


    # ===== ===== ===== inner functions ===== ===== =====

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


    # ===== ===== ===== slot functions ===== ===== =====
    
    def slot_change_rgb_visibility(self, visibility):
        for idx in range(5):
            rgb_gbox = getattr(self, "gbox_RGB_{}".format(idx))
            rgb_gbox.setVisible(visibility)
    
    def slot_change_hsv_visibility(self, visibility):
        for idx in range(5):
            hsv_gbox = getattr(self, "gbox_HSV_{}".format(idx))
            hsv_gbox.setVisible(visibility)
