# -*- coding: utf-8 -*-

import os
import time
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QGroupBox, QCheckBox, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from clibs.export import export_list, export_text, export_swatch
from clibs.color import Color


class Script(QWidget):
    """
    Script object based on QWidget. Init a script in script.
    """

    ps_filter = pyqtSignal(tuple)
    ps_enhance = pyqtSignal(tuple)
    ps_crop = pyqtSignal(bool)
    ps_replace = pyqtSignal(int)

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
        scroll_grid_layout.addWidget(self._zoom_gbox, 2, 1, 1, 1)

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
        scroll_grid_layout.addWidget(self._crop_gbox, 1, 1, 1, 1)

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

        # replace functional region.
        self._replace_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._replace_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._replace_gbox, 3, 1, 1, 1)

        self.btn_replace_rgb = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_rgb, 0, 1, 1, 1)
        self.btn_replace_rgb.clicked.connect(lambda x: self.ps_replace.emit(1))

        self.btn_replace_hsv = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_hsv, 1, 1, 1, 1)
        self.btn_replace_hsv.clicked.connect(lambda x: self.ps_replace.emit(2))

        self.btn_replace_cancel = QPushButton(self._replace_gbox)
        gbox_grid_layout.addWidget(self.btn_replace_cancel, 2, 1, 1, 1)
        self.btn_replace_cancel.clicked.connect(lambda x: self.ps_replace.emit(0))

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)

        # enhance functional region.
        self._enhance_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._enhance_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._enhance_gbox, 4, 1, 1, 1)

        self.lab_link = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_link, 0, 1, 1, 3)

        self.ckb_r = QCheckBox(self._enhance_gbox)
        self.ckb_r.setText("R")
        self.ckb_r.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_r, 1, 1, 1, 1)
        self.ckb_r.stateChanged.connect(self.unckeck_hsv)

        self.ckb_g = QCheckBox(self._enhance_gbox)
        self.ckb_g.setText("G")
        self.ckb_g.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_g, 1, 2, 1, 1)
        self.ckb_g.stateChanged.connect(self.unckeck_hsv)

        self.ckb_b = QCheckBox(self._enhance_gbox)
        self.ckb_b.setText("B")
        self.ckb_b.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_b, 1, 3, 1, 1)
        self.ckb_b.stateChanged.connect(self.unckeck_hsv)

        self.ckb_h = QCheckBox(self._enhance_gbox)
        self.ckb_h.setText("H")
        self.ckb_h.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_h, 2, 1, 1, 1)
        self.ckb_h.stateChanged.connect(self.uncheck_rgb)

        self.ckb_s = QCheckBox(self._enhance_gbox)
        self.ckb_s.setText("S")
        self.ckb_s.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_s, 2, 2, 1, 1)
        self.ckb_s.stateChanged.connect(self.uncheck_rgb)

        self.ckb_v = QCheckBox(self._enhance_gbox)
        self.ckb_v.setText("V")
        self.ckb_v.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_v, 2, 3, 1, 1)
        self.ckb_v.stateChanged.connect(self.uncheck_rgb)

        self.ckb_reserve = QCheckBox(self._enhance_gbox)
        self.ckb_reserve.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve, 3, 1, 1, 3)

        self.lab_sepr = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_sepr, 4, 1, 1, 3)

        self.sdr_sepr = QSlider(self._enhance_gbox)
        self.sdr_sepr.setOrientation(Qt.Horizontal)
        self.sdr_sepr.setMaximum(1000)
        self.sdr_sepr.setSingleStep(5)
        self.sdr_sepr.setPageStep(0)
        self.sdr_sepr.setTickPosition(QSlider.TicksAbove)
        self.sdr_sepr.setTickInterval(200)
        self.sdr_sepr.setValue(0)
        gbox_grid_layout.addWidget(self.sdr_sepr, 5, 1, 1, 3)
        self.sdr_sepr.valueChanged.connect(self.update_enhance)

        self.lab_fact = QLabel(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.lab_fact, 6, 1, 1, 3)

        self.sdr_fact = QSlider(self._enhance_gbox)
        self.sdr_fact.setOrientation(Qt.Horizontal)
        self.sdr_fact.setMaximum(1000)
        self.sdr_fact.setSingleStep(5)
        self.sdr_fact.setPageStep(0)
        self.sdr_fact.setTickPosition(QSlider.TicksAbove)
        self.sdr_fact.setTickInterval(200)
        self.sdr_fact.setValue(0)
        gbox_grid_layout.addWidget(self.sdr_fact, 7, 1, 1, 3)
        self.sdr_fact.valueChanged.connect(self.update_enhance)

        self.btn_enhs = QPushButton(self._enhance_gbox)
        gbox_grid_layout.addWidget(self.btn_enhs, 8, 1, 1, 3)
        self.btn_enhs.clicked.connect(self.emit_enhance)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 9, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 9, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 9, 4, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 230)

    def uncheck_rgb(self, state):
        if state:
            self.ckb_r.setChecked(False)
            self.ckb_g.setChecked(False)
            self.ckb_b.setChecked(False)

    def unckeck_hsv(self, state):
        if state:
            self.ckb_h.setChecked(False)
            self.ckb_s.setChecked(False)
            self.ckb_v.setChecked(False)

    def emit_enhance(self, value):
        """
        Emit enhance.
        """

        region = set()

        if self.ckb_r.isChecked() or self.ckb_g.isChecked() or self.ckb_b.isChecked():
            if self.ckb_r.isChecked():
                region.add(0)

            if self.ckb_g.isChecked():
                region.add(1)

            if self.ckb_b.isChecked():
                region.add(2)

            self.ps_enhance.emit(("rgb", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve.isChecked()))

        elif self.ckb_h.isChecked() or self.ckb_s.isChecked() or self.ckb_v.isChecked():
            if self.ckb_h.isChecked():
                region.add(0)

            if self.ckb_s.isChecked():
                region.add(1)

            if self.ckb_v.isChecked():
                region.add(2)

            self.ps_enhance.emit(("hsv", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve.isChecked()))

    def update_enhance(self):
        """
        Update enhance region.
        """

        self.lab_sepr.setText(self._enhance_descs[1].format(self.sdr_sepr.value() / 10))
        self.lab_fact.setText(self._enhance_descs[2].format(self.sdr_fact.value() / 10))

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

        self._replace_gbox.setTitle(self._gbox_descs[4])
        self.btn_replace_rgb.setText(self._replace_descs[0])
        self.btn_replace_hsv.setText(self._replace_descs[1])
        self.btn_replace_cancel.setText(self._replace_descs[2])

        self._enhance_gbox.setTitle(self._gbox_descs[3])
        self.lab_link.setText(self._enhance_descs[0])
        self.btn_enhs.setText(self._enhance_descs[3])
        self.ckb_reserve.setText(self._enhance_descs[4])
        self.update_enhance()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Script", "Filter"),
            _translate("Script", "Zoom"),
            _translate("Script", "Crop"),
            _translate("Script", "Enhance"),
            _translate("Script", "Replace"),
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

        self._replace_descs = (
            _translate("Script", "Replace RGB"),
            _translate("Script", "Replace HSV"),
            _translate("Script", "Cancel"),
        )

        self._enhance_descs = (
            _translate("Script", "Link"),
            _translate("Script", "Border - {:.1f}%"),
            _translate("Script", "Factor - {:.1f}%"),
            _translate("Script", "Enhance"),
            _translate("Script", "Reserve Result"),
        )
