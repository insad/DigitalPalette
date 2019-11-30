# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QLabel, QShortcut
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QCursor, QKeySequence
from clibs.color import Color


class EmptyCell(QWidget):
    """
    EmptyCell objet based on QWidget. Init an empty unit cell in depot.
    """

    ps_selected = pyqtSignal(int)
    ps_dclicked = pyqtSignal(int)
    ps_informed = pyqtSignal(int)

    def __init__(self, wget, args, idx):
        """
        Init empty unit cell.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self.idx = idx
        self.colors = (None, None, None, None, None)
        self.activated = False
        self.outer_box = (0, 0, 0, 0)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()

        cs_wid = int(min(wid, hig) * self._args.coset_ratio / 2)

        cs_boxes = [
            (wid / 2 - cs_wid, hig / 2 - cs_wid, cs_wid, cs_wid),
            (wid / 2, hig / 2 - cs_wid, cs_wid, cs_wid),
            (wid / 2 - cs_wid, hig / 2, cs_wid, cs_wid),
            (wid / 2, hig / 2, cs_wid, cs_wid),
            (wid / 2 - cs_wid / 2, hig / 2 - cs_wid / 2, cs_wid, cs_wid),
        ]

        self.outer_box = (wid / 2 - cs_wid, hig / 2 - cs_wid, cs_wid * 2, cs_wid * 2)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        for idx in range(5):
            if self.activated:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            if self.colors[4 - idx] != None:
                rgb = Color.hsv2rgb(self.colors[4 - idx])
                painter.setBrush(QColor(*rgb))

            else:
                painter.setBrush(QBrush(Qt.NoBrush))

            painter.drawRoundedRect(*cs_boxes[idx], cs_wid / 12, cs_wid / 12)

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        point = (event.x(), event.y())

        if self.outer_box[0] < point[0] < self.outer_box[0] + self.outer_box[2] and self.outer_box[1] < point[1] < self.outer_box[1] + self.outer_box[3]:
            if event.button() == Qt.LeftButton:
                self.ps_selected.emit(self.idx)

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton:
                self.ps_informed.emit(self.idx)

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = (event.x(), event.y())

            if self.outer_box[0] < point[0] < self.outer_box[0] + self.outer_box[2] and self.outer_box[1] < point[1] < self.outer_box[1] + self.outer_box[3]:
                self.ps_dclicked.emit(self.idx)

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()


class UnitCell(EmptyCell):
    """
    UnitCell objet based on EmptyCell. Init a color set unit cell in palette.
    """

    def __init__(self, wget, args, idx):
        """
        Init unit cell.
        """

        super().__init__(wget, args, idx)

        # load args.
        self.colors, self.hm_rule, self.desc = self._args.stab_cslist[self.idx]


class Depot(QWidget):
    """
    Depot object based on QWidget. Init a color set depot in workarea.
    """

    ps_update = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init color set depot.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self._current_idx = None
 
        # load translations.
        self._func_tr_()

        # init qt args.
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea(self)
        self._scroll_area.setFrameShape(QFrame.Box)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setWidgetResizable(True)
        grid_layout.addWidget(self._scroll_area)

        self._scroll_bar = self._scroll_area.verticalScrollBar()

        self._scroll_contents = QWidget()
        self._scroll_grid_layout = QGridLayout(self._scroll_contents)
        self._scroll_grid_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setWidget(self._scroll_contents)

        self._unitcells = []

        for idx in range(len(self._args.stab_cslist)):
            unitcell = UnitCell(self._scroll_contents, self._args, idx)
            unitcell.ps_selected.connect(self.activate_idx)
            unitcell.ps_dclicked.connect(self.import_idx)
            self._scroll_grid_layout.addWidget(unitcell)
            self._unitcells.append(unitcell)

        emptycell = EmptyCell(self._scroll_contents, self._args, len(self._args.stab_cslist))
        emptycell.ps_selected.connect(self.activate_idx)
        emptycell.ps_dclicked.connect(lambda x: self.attach_set())
        self._unitcells.append(emptycell)

        shortcut = QShortcut(QKeySequence("Del"), self)
        shortcut.activated.connect(self.delete_set)
        shortcut = QShortcut(QKeySequence("d"), self)
        shortcut.activated.connect(self.delete_set)

        shortcut = QShortcut(QKeySequence("Insert"), self)
        shortcut.activated.connect(self.insert_set)
        shortcut = QShortcut(QKeySequence("i"), self)
        shortcut.activated.connect(self.insert_set)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        pl_wid = self.geometry().width() / self._args.stab_column
        pl_wid = pl_wid if pl_wid < self.geometry().height() * 0.95 else self.geometry().height() * 0.95
        tot_rows = len(self._unitcells) // self._args.stab_column if len(self._unitcells) % self._args.stab_column == 0 else len(self._unitcells) // self._args.stab_column + 1

        self._scroll_contents.setMinimumSize(pl_wid * self._args.stab_column, pl_wid * tot_rows)
        self._scroll_contents.setMaximumSize(pl_wid * self._args.stab_column, pl_wid * tot_rows)

        for i in range(tot_rows):
            for j in range(self._args.stab_column):
                idx = self._args.stab_column * i + j

                if idx < len(self._unitcells):
                    self._unitcells[idx].setGeometry(pl_wid * j, pl_wid * i, pl_wid, pl_wid)

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        self.activate_idx(None)

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def activate_idx(self, idx):
        """
        Activate num idx unitcell and deactivate other unitcells.
        """

        if self._current_idx != None:
            self._unitcells[self._current_idx].activated = False
            self._unitcells[self._current_idx].update()

        self._current_idx = idx

        if self._current_idx != None:
            self._current_idx = self._current_idx if self._current_idx > 0 else 0
            self._current_idx = self._current_idx if self._current_idx < len(self._unitcells) else len(self._unitcells) - 1

            self._unitcells[self._current_idx].activated = True
            self._unitcells[self._current_idx].update()

            upp_pos = self._scroll_contents.geometry().y() + self._unitcells[self._current_idx].geometry().y()
            low_pos = self._scroll_contents.geometry().y() + self._unitcells[self._current_idx].geometry().y() + self._unitcells[self._current_idx].geometry().height()

            if upp_pos < 0 or low_pos > self._scroll_area.geometry().height():
                self._scroll_bar.setValue(self._unitcells[self._current_idx].geometry().y())

            """
            if low_pos > self._scroll_area.geometry().height():
                self._scroll_bar.setValue(self._unitcells[self._current_idx].geometry().y() + self._unitcells[self._current_idx].geometry().height() - self._scroll_area.geometry().height())
            """

    def import_idx(self, idx):
        """
        Import colors in num idx unitcell into color wheel.
        """

        self._args.sys_color_set.import_color_set(self._unitcells[idx].colors, tp="hsv")
        self._args.hm_rule = self._unitcells[idx].hm_rule

        self.ps_update.emit(True)

    def move(self, shift_x, shift_y):
        """
        Select unitcell around current idx unitcell.
        """

        if not self.isVisible():
            return

        if self._current_idx == None:
            self.activate_idx(0)

        elif shift_x < 0:
            self.activate_idx(self._current_idx - 1)

        elif shift_x > 0:
            self.activate_idx(self._current_idx + 1)

        elif shift_y < 0:
            self.activate_idx(self._current_idx - self._args.stab_column)

        elif shift_y > 0:
            self.activate_idx(self._current_idx + self._args.stab_column)

    def zoom(self, ratio):
        """
        Increase or decrease columns for display.
        """

        if not self.isVisible():
            return

        if ratio > 1:
            self._args.stab_column -= 1

        elif ratio < 1:
            self._args.stab_column += 1

        self._args.stab_column = self._args.stab_column if self._args.stab_column > 1 else 1
        self._args.stab_column = self._args.stab_column if self._args.stab_column < 9 else 9

        self.update()
        self.activate_idx(self._current_idx)

    def home(self):
        """
        Locate current unitcell.
        """

        if not self.isVisible():
            return

        self.activate_idx(self._current_idx)

    def insert_set(self):
        """
        Insert current color set.
        """

        if not self.isVisible():
            return

        if self._current_idx == None:
            return

        if self._current_idx == len(self._args.stab_cslist):
            self.attach_set()

        else:
            self.import_idx(self._current_idx)

    def delete_set(self):
        """
        Delete current color set from depot.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx >= len(self._args.stab_cslist):
            return

        self._unitcells[self._current_idx].close()
        self._unitcells.pop(self._current_idx)
        self._args.stab_cslist.pop(self._current_idx)

        for i in range(len(self._unitcells) - self._current_idx):
            self._unitcells[self._current_idx + i].idx = self._current_idx + i

        self._unitcells[self._current_idx].activated = True
        self.update()

    def attach_set(self):
        """
        Attach current color set into depot.
        """

        if not self.isVisible():
            return

        colors = (self._args.sys_color_set[0].hsv, self._args.sys_color_set[1].hsv, self._args.sys_color_set[2].hsv, self._args.sys_color_set[3].hsv, self._args.sys_color_set[4].hsv)
        self._args.stab_cslist.append((colors, self._args.hm_rule, "None"))

        unitcell = UnitCell(self._scroll_contents, self._args, len(self._unitcells) - 1)
        unitcell.activated = True
        unitcell.ps_selected.connect(self.activate_idx)
        unitcell.ps_dclicked.connect(self.import_idx)

        emptycell = self._unitcells[len(self._unitcells) - 1]
        emptycell.idx = len(self._unitcells)
        emptycell.activated = False

        self._scroll_grid_layout.addWidget(unitcell)
        self._unitcells[len(self._unitcells) - 1] = unitcell
        self._unitcells.append(emptycell)

        self.update()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Depot", "Attach"),
            _translate("Depot", "Import"),
            _translate("Depot", "Export"),
            _translate("Depot", "Delete"),
            _translate("Depot", "Detail"),
        )
