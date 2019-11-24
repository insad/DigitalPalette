# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QCheckBox, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QSize, pyqtSignal


class Mode(QWidget):
    """
    Mode object based on QWidget. Init a mode in mode.
    """

    ps_mode_changed = pyqtSignal(bool)

    def __init__(self, args):
        """
        Init mode.
        """

        super().__init__()

        # load args.
        self._args = args

        # init qt args.
        mode_grid_layout = QGridLayout(self)
        mode_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setWidgetResizable(True)
        mode_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        self._cbox_rgb = QCheckBox(scroll_contents)
        self._cbox_rgb.setText("RGB")
        scroll_grid_layout.addWidget(self._cbox_rgb, 0, 1, 1, 1)
        self._cbox_rgb.stateChanged.connect(self.modify_state("rgb"))

        self._cbox_hsv = QCheckBox(scroll_contents)
        self._cbox_hsv.setText("HSV")
        scroll_grid_layout.addWidget(self._cbox_hsv, 1, 1, 1, 1)
        self._cbox_hsv.stateChanged.connect(self.modify_state("hsv"))

        self.update_mode()

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 2, 2, 1, 1)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(180, 90)

    def modify_state(self, tag):
        """
        Modify stored shown state set by cbox.
        """

        def _func_(state):
            setattr(self._args, "show_{}".format(tag), bool(state))

            self.ps_mode_changed.emit(True)

        return _func_

    def update_mode(self):
        """
        Update mode cbox by self._args.show_rgb and show_hsv.
        """

        self._cbox_rgb.setChecked(self._args.show_rgb)
        self._cbox_hsv.setChecked(self._args.show_hsv)
