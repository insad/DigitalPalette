# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QShortcut, QCheckBox, QLabel, QSlider
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QCoreApplication
from PyQt5.QtGui import QKeySequence


class Transformation(QWidget):
    """
    Transformation object based on QWidget. Init a transformation in transformation.
    """

    ps_move = pyqtSignal(tuple)
    ps_zoom = pyqtSignal(float)
    ps_home = pyqtSignal(bool)
    ps_replace = pyqtSignal(int)
    ps_enhance = pyqtSignal(tuple)

    def __init__(self, wget, args):
        """
        Init transformation.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        zoom_grid_layout = QGridLayout(self)
        zoom_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        zoom_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(4)
        scroll_grid_layout.setVerticalSpacing(4)
        scroll_area.setWidget(scroll_contents)

        # move functional region.
        self._move_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._move_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._move_gbox, 0, 1, 1, 1)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↑")
        gbox_grid_layout.addWidget(btn, 0, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_up())

        shortcut = QShortcut(QKeySequence("Up"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↓")
        gbox_grid_layout.addWidget(btn, 2, 2, 1, 1)
        btn.clicked.connect(lambda x: self.move_down())

        shortcut = QShortcut(QKeySequence("Down"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("←")
        gbox_grid_layout.addWidget(btn, 1, 1, 1, 1)
        btn.clicked.connect(lambda x: self.move_left())

        shortcut = QShortcut(QKeySequence("Left"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("→")
        gbox_grid_layout.addWidget(btn, 1, 3, 1, 1)
        btn.clicked.connect(lambda x: self.move_right())

        shortcut = QShortcut(QKeySequence("Right"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(self._move_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↺")
        gbox_grid_layout.addWidget(btn, 1, 2, 1, 1)
        btn.clicked.connect(lambda x: self.ps_home.emit(True))

        shortcut = QShortcut(QKeySequence("Home"), self)
        shortcut.activated.connect(btn.click)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 3, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 3, 4, 1, 1)

        # zoom functional region.
        self._zoom_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._zoom_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._zoom_gbox, 1, 1, 1, 1)

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("+")
        gbox_grid_layout.addWidget(btn, 0, 1, 1, 1)
        btn.clicked.connect(lambda x: self.ps_zoom.emit(self._args.zoom_step))

        shortcut = QShortcut(QKeySequence("="), self)
        shortcut.activated.connect(btn.click)

        shortcut = QShortcut(QKeySequence("]"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(self._zoom_gbox)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("–")
        gbox_grid_layout.addWidget(btn, 0, 3, 1, 1)
        btn.clicked.connect(lambda x: self.ps_zoom.emit(1 / self._args.zoom_step))

        shortcut = QShortcut(QKeySequence("-"), self)
        shortcut.activated.connect(btn.click)

        shortcut = QShortcut(QKeySequence("["), self)
        shortcut.activated.connect(btn.click)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 1, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 1, 4, 1, 1)

        # replace functional region.
        self._replace_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._replace_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._replace_gbox, 2, 1, 1, 1)

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
        scroll_grid_layout.addWidget(self._enhance_gbox, 3, 1, 1, 1)

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
        self.ckb_reserve.stateChanged.connect(self.sync_reserve)

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

        # inverse functional region.
        self._inverse_gbox = QGroupBox(scroll_contents)
        gbox_grid_layout = QGridLayout(self._inverse_gbox)
        gbox_grid_layout.setContentsMargins(8, 8, 8, 8)
        gbox_grid_layout.setHorizontalSpacing(8)
        gbox_grid_layout.setVerticalSpacing(12)
        scroll_grid_layout.addWidget(self._inverse_gbox, 4, 1, 1, 1)

        self.lab_link_inv = QLabel(self._inverse_gbox)
        gbox_grid_layout.addWidget(self.lab_link_inv, 0, 1, 1, 3)

        self.ckb_r_inv = QCheckBox(self._inverse_gbox)
        self.ckb_r_inv.setText("R")
        self.ckb_r_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_r_inv, 1, 1, 1, 1)
        self.ckb_r_inv.stateChanged.connect(self.unckeck_hsv_inv)

        self.ckb_g_inv = QCheckBox(self._inverse_gbox)
        self.ckb_g_inv.setText("G")
        self.ckb_g_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_g_inv, 1, 2, 1, 1)
        self.ckb_g_inv.stateChanged.connect(self.unckeck_hsv_inv)

        self.ckb_b_inv = QCheckBox(self._inverse_gbox)
        self.ckb_b_inv.setText("B")
        self.ckb_b_inv.setChecked(True)
        gbox_grid_layout.addWidget(self.ckb_b_inv, 1, 3, 1, 1)
        self.ckb_b_inv.stateChanged.connect(self.unckeck_hsv_inv)

        self.ckb_h_inv = QCheckBox(self._inverse_gbox)
        self.ckb_h_inv.setText("H")
        self.ckb_h_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_h_inv, 2, 1, 1, 1)
        self.ckb_h_inv.stateChanged.connect(self.uncheck_rgb_inv)

        self.ckb_s_inv = QCheckBox(self._inverse_gbox)
        self.ckb_s_inv.setText("S")
        self.ckb_s_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_s_inv, 2, 2, 1, 1)
        self.ckb_s_inv.stateChanged.connect(self.uncheck_rgb_inv)

        self.ckb_v_inv = QCheckBox(self._inverse_gbox)
        self.ckb_v_inv.setText("V")
        self.ckb_v_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_v_inv, 2, 3, 1, 1)
        self.ckb_v_inv.stateChanged.connect(self.uncheck_rgb_inv)

        self.ckb_reserve_inv = QCheckBox(self._inverse_gbox)
        self.ckb_reserve_inv.setChecked(False)
        gbox_grid_layout.addWidget(self.ckb_reserve_inv, 3, 1, 1, 3)
        self.ckb_reserve_inv.stateChanged.connect(self.sync_reserve)

        self.btn_invs = QPushButton(self._inverse_gbox)
        gbox_grid_layout.addWidget(self.btn_invs, 4, 1, 1, 3)
        self.btn_invs.clicked.connect(self.emit_inverse)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        gbox_grid_layout.addItem(spacer, 5, 1, 1, 3)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum)
        gbox_grid_layout.addItem(spacer, 5, 4, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(185, 90)

    def move_up(self):
        """
        Move image up.
        """

        if self._args.rev_direct:
            self.ps_move.emit((0, self._args.move_step))

        else:
            self.ps_move.emit((0, self._args.move_step * -1))

    def move_down(self):
        """
        Move image down.
        """

        if self._args.rev_direct:
            self.ps_move.emit((0, self._args.move_step * -1))

        else:
            self.ps_move.emit((0, self._args.move_step))

    def move_left(self):
        """
        Move image left.
        """

        if self._args.rev_direct:
            self.ps_move.emit((self._args.move_step, 0))

        else:
            self.ps_move.emit((self._args.move_step * -1, 0))

    def move_right(self):
        """
        Move image right.
        """

        if self._args.rev_direct:
            self.ps_move.emit((self._args.move_step * -1, 0))

        else:
            self.ps_move.emit((self._args.move_step, 0))

    def uncheck_rgb(self, state):
        """
        Uncheck all r, g, b boxes for enhance.
        """

        if state:
            self.ckb_r.setChecked(False)
            self.ckb_g.setChecked(False)
            self.ckb_b.setChecked(False)

    def unckeck_hsv(self, state):
        """
        Uncheck all h, s, v boxes for enhance.
        """

        if state:
            self.ckb_h.setChecked(False)
            self.ckb_s.setChecked(False)
            self.ckb_v.setChecked(False)

    def uncheck_rgb_inv(self, state):
        """
        Uncheck all r, g, b boxes for inverse.
        """

        if state:
            self.ckb_r_inv.setChecked(False)
            self.ckb_g_inv.setChecked(False)
            self.ckb_b_inv.setChecked(False)

    def unckeck_hsv_inv(self, state):
        """
        Uncheck all h, s, v boxes for inverse.
        """

        if state:
            self.ckb_h_inv.setChecked(False)
            self.ckb_s_inv.setChecked(False)
            self.ckb_v_inv.setChecked(False)

    def sync_reserve(self, state):
        """
        Sync enhance and inverse reserve boxes.
        """

        if state != self.ckb_reserve.isChecked():
            self.ckb_reserve.setChecked(state)

        if state != self.ckb_reserve_inv.isChecked():
            self.ckb_reserve_inv.setChecked(state)

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

            self.ps_enhance.emit(("enhance_rgb", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve.isChecked()))

        elif self.ckb_h.isChecked() or self.ckb_s.isChecked() or self.ckb_v.isChecked():
            if self.ckb_h.isChecked():
                region.add(0)

            if self.ckb_s.isChecked():
                region.add(1)

            if self.ckb_v.isChecked():
                region.add(2)

            self.ps_enhance.emit(("enhance_hsv", region, self.sdr_sepr.value() / 1000, self.sdr_fact.value() / 1000, self.ckb_reserve.isChecked()))

    def emit_inverse(self, value):
        """
        Emit inverse.
        """

        region = set()

        if self.ckb_r_inv.isChecked() or self.ckb_g_inv.isChecked() or self.ckb_b_inv.isChecked():
            if self.ckb_r_inv.isChecked():
                region.add(0)

            if self.ckb_g_inv.isChecked():
                region.add(1)

            if self.ckb_b_inv.isChecked():
                region.add(2)

            self.ps_enhance.emit(("inverse_rgb", region, self.ckb_reserve_inv.isChecked()))

        elif self.ckb_h_inv.isChecked() or self.ckb_s_inv.isChecked() or self.ckb_v_inv.isChecked():
            if self.ckb_h_inv.isChecked():
                region.add(0)

            if self.ckb_s_inv.isChecked():
                region.add(1)

            if self.ckb_v_inv.isChecked():
                region.add(2)

            self.ps_enhance.emit(("inverse_hsv", region, self.ckb_reserve_inv.isChecked()))

    def update_enhance(self):
        """
        Update enhance region.
        """

        self.lab_sepr.setText(self._enhance_descs[1].format(self.sdr_sepr.value() / 10))
        self.lab_fact.setText(self._enhance_descs[2].format(self.sdr_fact.value() / 10))

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._move_gbox.setTitle(self._gbox_descs[0])
        self._zoom_gbox.setTitle(self._gbox_descs[1])

        self._replace_gbox.setTitle(self._gbox_descs[2])
        self.btn_replace_rgb.setText(self._replace_descs[0])
        self.btn_replace_hsv.setText(self._replace_descs[1])
        self.btn_replace_cancel.setText(self._replace_descs[2])

        self._enhance_gbox.setTitle(self._gbox_descs[3])
        self.lab_link.setText(self._enhance_descs[0])
        self.ckb_reserve.setText(self._enhance_descs[3])
        self.btn_enhs.setText(self._enhance_descs[4])
        self.update_enhance()

        self._inverse_gbox.setTitle(self._gbox_descs[4])
        self.lab_link_inv.setText(self._enhance_descs[0])
        self.ckb_reserve_inv.setText(self._enhance_descs[3])
        self.btn_invs.setText(self._enhance_descs[5])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._gbox_descs = (
            _translate("Transformation", "Move"),
            _translate("Transformation", "Zoom"),
            _translate("Transformation", "Replace"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
        )

        self._replace_descs = (
            _translate("Transformation", "Replace RGB"),
            _translate("Transformation", "Replace HSV"),
            _translate("Transformation", "Cancel"),
        )

        self._enhance_descs = (
            _translate("Transformation", "Link"),
            _translate("Transformation", "Border - {:.1f}%"),
            _translate("Transformation", "Factor - {:.1f}%"),
            _translate("Transformation", "Reserve Result"),
            _translate("Transformation", "Enhance"),
            _translate("Transformation", "Inverse"),
        )
