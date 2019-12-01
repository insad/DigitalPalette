# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QShortcut
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QKeySequence


class Transformation(QWidget):
    """
    Transformation object based on QWidget. Init a transformation in transformation.
    """

    ps_move = pyqtSignal(tuple)
    ps_zoom = pyqtSignal(float)
    ps_home = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init transformation.
        """

        super().__init__(wget)

        # load args.
        self._args = args

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

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↑")
        scroll_grid_layout.addWidget(btn, 0, 2, 1, 1)
        btn.clicked.connect(lambda x: self.ps_move.emit((0, self._args.move_step * -1)))

        shortcut = QShortcut(QKeySequence("Up"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↓")
        scroll_grid_layout.addWidget(btn, 2, 2, 1, 1)
        btn.clicked.connect(lambda x: self.ps_move.emit((0, self._args.move_step)))

        shortcut = QShortcut(QKeySequence("Down"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("←")
        scroll_grid_layout.addWidget(btn, 1, 1, 1, 1)
        btn.clicked.connect(lambda x: self.ps_move.emit((self._args.move_step * -1, 0)))

        shortcut = QShortcut(QKeySequence("Left"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("→")
        scroll_grid_layout.addWidget(btn, 1, 3, 1, 1)
        btn.clicked.connect(lambda x: self.ps_move.emit((self._args.move_step, 0)))

        shortcut = QShortcut(QKeySequence("Right"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("↺")
        scroll_grid_layout.addWidget(btn, 1, 2, 1, 1)
        btn.clicked.connect(lambda x: self.ps_home.emit(True))

        shortcut = QShortcut(QKeySequence("Home"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("+")
        scroll_grid_layout.addWidget(btn, 4, 1, 1, 1)
        btn.clicked.connect(lambda x: self.ps_zoom.emit(self._args.zoom_step))

        shortcut = QShortcut(QKeySequence("="), self)
        shortcut.activated.connect(btn.click)

        shortcut = QShortcut(QKeySequence("]"), self)
        shortcut.activated.connect(btn.click)

        btn = QPushButton(scroll_contents)
        btn.setMinimumSize(30, 30)
        btn.setMaximumSize(30, 30)
        btn.setText("–")
        scroll_grid_layout.addWidget(btn, 4, 3, 1, 1)
        btn.clicked.connect(lambda x: self.ps_zoom.emit(1 / self._args.zoom_step))

        shortcut = QShortcut(QKeySequence("-"), self)
        shortcut.activated.connect(btn.click)

        shortcut = QShortcut(QKeySequence("["), self)
        shortcut.activated.connect(btn.click)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 5, 2, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 5, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 5, 4, 1, 1)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(180, 90)
