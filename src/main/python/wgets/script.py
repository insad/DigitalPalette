# -*- coding: utf-8 -*-

import os
import time
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QGroupBox, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from clibs.export import export_list, export_text, export_swatch
from clibs.color import Color


class Script(QWidget):
    """
    Script object based on QWidget. Init a script in script.
    """

    ps_filter = pyqtSignal(tuple)
    ps_crop = pyqtSignal(bool)
    ps_freeze = pyqtSignal(bool)
    ps_print = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init operation.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        script_grid_layout = QGridLayout(self)
        script_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        script_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        # filter functional region.
        self._filter_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._filter_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._filter_gbox, 0, 1, 1, 1)

        self._filter_btns = []
        for i in range(10):
            btn = QPushButton(self._filter_gbox)
            self._filter_btns.append(btn)

        gbox_grid_layout.addWidget(self._filter_btns[0], 0, 1, 1, 1)
        self._filter_btns[0].clicked.connect(lambda x: self.ps_filter.emit(("BLUR", None)))

        gbox_grid_layout.addWidget(self._filter_btns[1], 1, 1, 1, 1)
        self._filter_btns[1].clicked.connect(lambda x: self.ps_filter.emit(("CONTOUR", None)))

        gbox_grid_layout.addWidget(self._filter_btns[2], 2, 1, 1, 1)
        self._filter_btns[2].clicked.connect(lambda x: self.ps_filter.emit(("DETAIL", None)))

        gbox_grid_layout.addWidget(self._filter_btns[3], 3, 1, 1, 1)
        self._filter_btns[3].clicked.connect(lambda x: self.ps_filter.emit(("EDGE_ENHANCE", None)))

        gbox_grid_layout.addWidget(self._filter_btns[4], 4, 1, 1, 1)
        self._filter_btns[4].clicked.connect(lambda x: self.ps_filter.emit(("EDGE_ENHANCE_MORE", None)))

        gbox_grid_layout.addWidget(self._filter_btns[5], 5, 1, 1, 1)
        self._filter_btns[5].clicked.connect(lambda x: self.ps_filter.emit(("EMBOSS", None)))

        gbox_grid_layout.addWidget(self._filter_btns[6], 6, 1, 1, 1)
        self._filter_btns[6].clicked.connect(lambda x: self.ps_filter.emit(("FIND_EDGES", None)))

        gbox_grid_layout.addWidget(self._filter_btns[7], 7, 1, 1, 1)
        self._filter_btns[7].clicked.connect(lambda x: self.ps_filter.emit(("SHARPEN", None)))

        gbox_grid_layout.addWidget(self._filter_btns[8], 8, 1, 1, 1)
        self._filter_btns[8].clicked.connect(lambda x: self.ps_filter.emit(("SMOOTH", None)))

        gbox_grid_layout.addWidget(self._filter_btns[9], 9, 1, 1, 1)
        self._filter_btns[9].clicked.connect(lambda x: self.ps_filter.emit(("SMOOTH_MORE", None)))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 10, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 10, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 10, 2, 1, 1)

        # zoom functional region.
        self._zoom_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._zoom_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._zoom_gbox, 3, 1, 1, 1)

        self.lab_zoom = QLabel(self._zoom_gbox)
        gbox_grid_layout.addWidget(self.lab_zoom, 0, 1, 1, 1)

        self.sdr_zoom = QSlider(self._zoom_gbox)
        self.sdr_zoom.setOrientation(Qt.Horizontal)
        self.sdr_zoom.setMaximum(100)
        self.sdr_zoom.setSingleStep(1)
        self.sdr_zoom.setPageStep(0)
        self.sdr_zoom.setTickPosition(QSlider.TicksAbove)
        self.sdr_zoom.setTickInterval(10)
        self.sdr_zoom.setValue(40)
        gbox_grid_layout.addWidget(self.sdr_zoom, 1, 1, 1, 1)
        self.sdr_zoom.valueChanged.connect(self.update_zoom)

        self.btn_zoom = QPushButton(self._zoom_gbox)
        gbox_grid_layout.addWidget(self.btn_zoom, 2, 1, 1, 1)
        self.btn_zoom.clicked.connect(lambda x: self.ps_filter.emit(("ZOOM", self.sdr_zoom.value() / 40)))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)

        # crop functional region.
        self._crop_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._crop_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._crop_gbox, 2, 1, 1, 1)

        self.btn_crop = QPushButton(self._crop_gbox)
        gbox_grid_layout.addWidget(self.btn_crop, 0, 1, 1, 1)
        self.btn_crop.clicked.connect(lambda x: self.ps_crop.emit(True))

        self.btn_cancel = QPushButton(self._crop_gbox)
        gbox_grid_layout.addWidget(self.btn_cancel, 1, 1, 1, 1)
        self.btn_cancel.clicked.connect(lambda x: self.ps_crop.emit(False))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)

        # snap functional region.
        self._snap_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._snap_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._snap_gbox, 1, 1, 1, 1)

        self.btn_freeze = QPushButton(self._snap_gbox)
        gbox_grid_layout.addWidget(self.btn_freeze, 0, 1, 1, 1)
        self.btn_freeze.clicked.connect(lambda x: self.ps_freeze.emit(True))

        self.btn_print = QPushButton(self._snap_gbox)
        gbox_grid_layout.addWidget(self.btn_print, 1, 1, 1, 1)
        self.btn_print.clicked.connect(lambda x: self.ps_print.emit(True))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 2, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 2, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 230)

    def update_zoom(self):
        """
        Update zoom region.
        """

        self.lab_zoom.setText(self._zoom_descs[0].format(self.sdr_zoom.value() / 40))

        if self.sdr_zoom.value() == 40:
            self.btn_zoom.setText(self._zoom_descs[1])

        elif self.sdr_zoom.value() < 40:
            self.btn_zoom.setText(self._zoom_descs[2])

        else:
            self.btn_zoom.setText(self._zoom_descs[3])

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._filter_gbox.setTitle(self._gbox_descs[0])

        for i in range(10):
            self._filter_btns[i].setText(self._filter_descs[i])

        self._zoom_gbox.setTitle(self._gbox_descs[1])
        self.update_zoom()

        self._crop_gbox.setTitle(self._gbox_descs[2])
        self.btn_crop.setText(self._crop_descs[0])
        self.btn_cancel.setText(self._crop_descs[1])

        self._snap_gbox.setTitle(self._gbox_descs[3])
        self.btn_freeze.setText(self._snap_descs[0])
        self.btn_print.setText(self._snap_descs[1])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Script", "Filter"),
            _translate("Script", "Zoom"),
            _translate("Script", "Crop"),
            _translate("Script", "Snap"),
        )

        self._filter_descs = (
            _translate("Script", "Blur"),
            _translate("Script", "Contour"),
            _translate("Script", "Detail"),
            _translate("Script", "Edge Enhance"),
            _translate("Script", "Edge Enhance More"),
            _translate("Script", "Emboss"),
            _translate("Script", "Find Edges"),
            _translate("Script", "Sharpen"),
            _translate("Script", "Smooth"),
            _translate("Script", "Smooth More"),
        )

        self._zoom_descs = (
            _translate("Script", "Ratio - {:.3f}"),
            _translate("Script", "Zoom"),
            _translate("Script", "Zoom In"),
            _translate("Script", "Zoom Out"),
        )

        self._crop_descs = (
            _translate("Script", "Crop"),
            _translate("Script", "Cancel"),
        )

        self._snap_descs = (
            _translate("Script", "Freeze"),
            _translate("Script", "Print"),
        )
