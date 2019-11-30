# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QScrollArea, QFrame, QColorDialog, QApplication, QShortcut
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QMimeData
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence
from cguis.design.scroll_cube import Ui_ScrollCube
from clibs.color import Color


class Square(QWidget):
    """
    Square objet based on QWidget. Init a color square in cube.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_index_changed = pyqtSignal(bool)

    def __init__(self, wget, args, idx):
        """
        Init color square.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._idx = idx

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()
        rto = (1.0 - self._args.cubic_ratio) / 2

        self._box = [wid * rto, hig * rto, wid * self._args.cubic_ratio, hig * self._args.cubic_ratio]

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self._idx == self._args.sys_activated_idx:
            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid * 1.5))
        else:
            painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid * 1.5))

        painter.setBrush(QColor(*self._args.sys_color_set[self._idx].rgb))
        painter.drawRect(*self._box)

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                self._args.sys_activated_idx = self._idx

                self.ps_index_changed.emit(True)

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                dialog = QColorDialog.getColor(QColor(*self._args.sys_color_set[self._idx].rgb))

                if dialog.isValid():
                    color = Color((dialog.red(), dialog.green(), dialog.blue()), tp="rgb", overflow=self._args.sys_color_set.get_overflow())
                    self._args.sys_color_set.modify(self._args.hm_rule, self._idx, color)

                    self.ps_color_changed.emit(True)

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()


class Cube(QWidget, Ui_ScrollCube):
    """
    Cube object based on QWidget. Init a color cube in table.
    """

    def __init__(self, wget, args, idx):
        """
        Init color cube.
        """

        super().__init__(wget)
        self.setupUi(self)

        # load args.
        self._args = args
        self._idx = idx

        # init qt args.
        cube_grid_layout = QGridLayout(self.cube_color)
        cube_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.square = Square(self.cube_color, self._args, self._idx)
        cube_grid_layout.addWidget(self.square)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.cube_color.geometry().width()
        self.cube_color.setMinimumHeight(wid * 3 / 5)


class CubeTable(QWidget):
    """
    CubeTable object based on QWidget. Init color cube table in result.
    """

    ps_color_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init color cube table.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._updated_colors = False

        # init qt args.
        cube_grid_layout = QGridLayout(self)
        cube_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        cube_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_horizontal_layout = QHBoxLayout(scroll_contents)
        scroll_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(scroll_contents)

        self._cubes = (
            Cube(scroll_contents, args, 0),
            Cube(scroll_contents, args, 1),
            Cube(scroll_contents, args, 2),
            Cube(scroll_contents, args, 3),
            Cube(scroll_contents, args, 4),
        )

        self.update_color()

        for idx in (2, 1, 0, 3, 4):
            scroll_horizontal_layout.addWidget(self._cubes[idx])
            self._cubes[idx].square.ps_color_changed.connect(lambda x: self.update_color())
            self._cubes[idx].square.ps_index_changed.connect(lambda x: self.update_index())

            for ctp in ("r", "g", "b"):
                obj = getattr(self._cubes[idx], "hs_rgb_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "direct", ctp))
                obj = getattr(self._cubes[idx], "sp_rgb_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "direct", ctp))

            for ctp in ("h", "s", "v"):
                obj = getattr(self._cubes[idx], "hs_hsv_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "indire", ctp))
                obj = getattr(self._cubes[idx], "dp_hsv_{}".format(ctp))
                obj.valueChanged.connect(self.modify_color(idx, "direct", ctp))

            self._cubes[idx].le_hec.textChanged.connect(self.modify_color(idx, "direct", "hec"))

        self.modify_box_visibility()

        shortcut = QShortcut(QKeySequence("r"), self)
        shortcut.activated.connect(self.clipboard("rgb"))

        shortcut = QShortcut(QKeySequence("h"), self)
        shortcut.activated.connect(self.clipboard("hsv"))

        shortcut = QShortcut(QKeySequence("c"), self)
        shortcut.activated.connect(self.clipboard("hec"))

        shortcut = QShortcut(QKeySequence("1"), self)
        shortcut.activated.connect(self.active_by_num(2))

        shortcut = QShortcut(QKeySequence("2"), self)
        shortcut.activated.connect(self.active_by_num(1))

        shortcut = QShortcut(QKeySequence("3"), self)
        shortcut.activated.connect(self.active_by_num(0))

        shortcut = QShortcut(QKeySequence("4"), self)
        shortcut.activated.connect(self.active_by_num(3))

        shortcut = QShortcut(QKeySequence("5"), self)
        shortcut.activated.connect(self.active_by_num(4))

    def sizeHint(self):
        return QSize(600, 150)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def modify_color(self, idx, kword, ctp):
        """
        Modify stored color set by slide and box name and value.
        """

        def _func_(value):
            if self._updated_colors:
                return

            if ctp == "hec":
                try:
                    value = Color.fmt_hec(value)
                except:
                    return

            self._updated_colors = True

            color = Color(self._args.sys_color_set[idx], tp="color", overflow=self._args.sys_color_set.get_overflow())
            if kword == "direct":
                color.setti(value, ctp)
            else:
                color.setti(value / 1E3, ctp)

            self._args.sys_color_set.modify(self._args.hm_rule, idx, color)
            self.update_color()

            self._updated_colors = False

        return _func_

    def update_color(self):
        """
        Update all colors.
        """

        self._updated_colors = True

        for lc_idx in range(5):
            for lc_ctp in ("r", "g", "b"):
                obj = getattr(self._cubes[lc_idx], "hs_rgb_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))
                obj = getattr(self._cubes[lc_idx], "sp_rgb_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))

            for lc_ctp in ("h", "s", "v"):
                obj = getattr(self._cubes[lc_idx], "hs_hsv_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp) * 1E3)
                obj = getattr(self._cubes[lc_idx], "dp_hsv_{}".format(lc_ctp))
                obj.setValue(self._args.sys_color_set[lc_idx].getti(lc_ctp))

            self._cubes[lc_idx].le_hec.setText(self._args.sys_color_set[lc_idx].getti("hec"))

        self.update_index()

        self._updated_colors = False

    def update_index(self):
        """
        Update color activated index.
        """

        for lc_idx in range(5):
            self._cubes[lc_idx].update()

        self.ps_color_changed.emit(True)

    def modify_rule(self):
        """
        Modify stored color set by rule selection.
        """

        self._args.sys_color_set.create(self._args.hm_rule)
        self.update_color()

    def create_set(self):
        """
        Create stored color set by create button.
        """

        self._args.sys_color_set.initialize()
        self._args.sys_color_set.create(self._args.hm_rule)
        self.update_color()

    def modify_box_visibility(self):
        """
        Modify the visibility of hsv or rgb cbox.
        """

        for i in range(5):
            self._cubes[i].gbox_hsv.setVisible(self._args.show_hsv)
            self._cubes[i].gbox_rgb.setVisible(self._args.show_rgb)

    def update_all(self):
        """
        Update five cubes and cube table.
        """

        for lc_idx in range(5):
            self._cubes[lc_idx].update()

        self.update()

    def clipboard(self, ctp):
        """
        Set the hec (hex code) values as the clipboard data by shortcut r, h and c.
        """

        def _func_():
            data = "["

            for i in (2, 1, 0, 3, 4):
                color = self._args.sys_color_set[i].getti(ctp)
                if ctp == "hec":
                    color = "'#{}'".format(color)
                data += str(color)
                data += ", "

            data = data[:-2] + "]"

            mimedata = QMimeData()
            mimedata.setText(data)

            clipboard = QApplication.clipboard()
            clipboard.setMimeData(mimedata)

        return _func_

    def active_by_num(self, idx):
        """
        Set activated idx by shortcut 1, 2, 3, 4 and 5.
        """

        def _func_():
            self._args.sys_activated_idx = idx
            self.update_index()

        return _func_
