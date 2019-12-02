# -*- coding: utf-8 -*-

import re
from PyQt5.QtWidgets import QWidget, QGridLayout, QScrollArea, QFrame, QShortcut, QMenu, QAction, QDialog, QDialogButtonBox, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QCursor, QKeySequence, QPixmap, QImage, QIcon
from cguis.design.info_dialog import Ui_InfoDialog
from cguis.resource import view_rc
from clibs.color import FakeColor, Color


class Info(QDialog, Ui_InfoDialog):
    """
    Info object based on QDialog. Init color set information.
    """
    
    def __init__(self, wget, args):
        """
        Init information.
        """

        super().__init__(wget)
        self.setupUi(self)

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        app_icon = QIcon()
        app_icon.addPixmap(QPixmap(":/images/images/icon_256.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(app_icon)

        self._clone = None
        self._unit_cell = UnitCell(self.colors, self._args, [None, None, None, None, None], "", "")

        color_grid_layout = QGridLayout(self.colors)
        color_grid_layout.setContentsMargins(1, 1, 1, 1)
        color_grid_layout.addWidget(self._unit_cell)

        # init buttons.
        self.buttonBox.clear()

        self._btn_1 = QPushButton()
        self._btn_1.clicked.connect(self.application)
        self.buttonBox.addButton(self._btn_1, QDialogButtonBox.AcceptRole)

        self._btn_2 = QPushButton()
        self._btn_2.clicked.connect(self.close)
        self.buttonBox.addButton(self._btn_2, QDialogButtonBox.RejectRole)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def clone_cell(self, unit_cell):
        self._clone = unit_cell

        self._unit_cell.color_set = unit_cell.color_set
        self._unit_cell.hm_rule = unit_cell.hm_rule
        context = unit_cell.desc.split("#")

        name = self._cell_desc[0]
        desc = ""

        for line in context:
            rline = line.lstrip().rstrip()

            if rline[:6] == "Name: ":
                name = re.split(r"\n\r\t\v\\\'\"\a\f", rline[6:])[0]
                name = name.lstrip().rstrip()

            elif rline[:6] == "Desc: ":
                desc = re.split(r"\v\\\'\"\a\f", rline[6:])[0]
                desc = desc.lstrip().rstrip()

        self.name_ledit.setText(name)
        self.desc_tedit.setText(desc)
        self.hm_rule_label.setText(self._rule_descs[self._args.global_hm_rules.index(unit_cell.hm_rule)])

    def application(self):
        self._clone.desc = "#Name: {} #Desc: {}".format(self.name_ledit.text(), self.desc_tedit.toPlainText())
        self._clone = None

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.setWindowTitle(self._dialog_desc[0])
        self._btn_1.setText(self._dialog_desc[1])
        self._btn_2.setText(self._dialog_desc[2])

        self.retranslateUi(self)

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._dialog_desc = (
            _translate("Info", "Information"),
            _translate("Info", "OK"),
            _translate("Info", "Cancel"),
        )

        self._cell_desc = (
            _translate("Info", "DigiPale Color Set"),
        )

        self._rule_descs = (
            _translate("Rule", "Analogous"),
            _translate("Rule", "Monochromatic"),
            _translate("Rule", "Triad"),
            _translate("Rule", "Tetrad"),
            _translate("Rule", "Pentad"),
            _translate("Rule", "Complementary"),
            _translate("Rule", "Shades"),
            _translate("Rule", "Custom"),
        )


class UnitCell(QWidget):
    """
    UnitCell objet based on QWidget. Init an unit cell in depot.
    """

    def __init__(self, wget, args, hsv_set, hm_rule, desc):
        """
        Init empty unit cell.
        """

        super().__init__(wget)

        # load args.
        self._args = args

        self.activated = False
        self.color_set = []

        for hsv in hsv_set:
            if hsv == None:
                self.color_set.append(hsv)

            else:
                self.color_set.append(FakeColor(tuple(Color.hsv2rgb(hsv).tolist()), hsv, Color.hsv2hec(hsv)))

        self.color_set = tuple(self.color_set)
        self.hm_rule = str(hm_rule)
        self.desc = str(desc)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()

        cs_wid = int(min(wid, hig) * self._args.coset_ratio / 2)

        cs_boxes = (
            (wid / 2 - cs_wid, hig / 2 - cs_wid, cs_wid, cs_wid),
            (wid / 2, hig / 2 - cs_wid, cs_wid, cs_wid),
            (wid / 2 - cs_wid, hig / 2, cs_wid, cs_wid),
            (wid / 2, hig / 2, cs_wid, cs_wid),
            (wid / 2 - cs_wid / 2, hig / 2 - cs_wid / 2, cs_wid, cs_wid),
        )

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self.activated:
            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
            painter.setBrush(QColor(Qt.white))
            painter.drawRoundedRect(self._args.positive_wid, self._args.positive_wid, wid - self._args.positive_wid * 2, hig - self._args.positive_wid * 2, wid / 9, hig / 9)

        for idx in range(5):
            if self.activated:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            if self.color_set[4 - idx] == None:
                painter.setBrush(QBrush(Qt.NoBrush))

            else:
                painter.setBrush(QColor(*self.color_set[4 - idx].rgb))

            painter.drawRoundedRect(*cs_boxes[idx], cs_wid / 9, cs_wid / 9)

        painter.end()


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

        self._left_click = False
        self._start_hig = None
        self._current_idx = None
        self._fetched_cell = None
 
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

        self.initialize()

        self._info = Info(self, self._args)

        self.create_menu()
        self.update_text()

        shortcut = QShortcut(QKeySequence("Del"), self)
        shortcut.activated.connect(self.delete_set)
        shortcut = QShortcut(QKeySequence("D"), self)
        shortcut.activated.connect(self.delete_set)

        shortcut = QShortcut(QKeySequence("Insert"), self)
        shortcut.activated.connect(self.insert_set)
        shortcut = QShortcut(QKeySequence("I"), self)
        shortcut.activated.connect(self.insert_set)

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        self._pl_wid = int((self.geometry().width() - 2) / self._args.stab_column)
        self._tot_rows = len(self._args.stab_ucells) // self._args.stab_column if len(self._args.stab_ucells) % self._args.stab_column == 0 else len(self._args.stab_ucells) // self._args.stab_column + 1

        height = self._pl_wid * self._tot_rows
        height = height if height > self.geometry().height() else self.geometry().height()

        self._scroll_contents.setMinimumSize(self._pl_wid * self._args.stab_column, height)
        self._scroll_contents.setMaximumSize(self._pl_wid * self._args.stab_column, height)

        for i in range(self._tot_rows):
            for j in range(self._args.stab_column):
                idx = self._args.stab_column * i + j

                if idx < len(self._args.stab_ucells) and isinstance(self._args.stab_ucells[idx], UnitCell):
                    self._args.stab_ucells[idx].setGeometry(self._pl_wid * j, self._pl_wid * i, self._pl_wid, self._pl_wid)

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        point = (event.x() - self._scroll_contents.geometry().x(), event.y() - self._scroll_contents.geometry().y())

        col = point[0] // self._pl_wid
        row = point[1] // self._pl_wid

        if col <= self._args.stab_column:
            idx = self._args.stab_column * row + col

            if event.button() == Qt.MidButton:
                self._start_hig = self._scroll_bar.value() + event.y()

            elif idx < len(self._args.stab_ucells):
                self.activate_idx(idx)

                if event.button() == Qt.LeftButton and idx < len(self._args.stab_ucells) - 1:
                    self._left_click = True

                    self._fetched_cell = self._args.stab_ucells[self._current_idx]
                    self._args.stab_ucells[self._current_idx] = None

                    self._fetched_cell.raise_()

                elif event.button() == Qt.RightButton:
                    if idx < len(self._args.stab_ucells) - 1:
                        self._info.clone_cell(self._args.stab_ucells[idx])

            else:
                self.activate_idx(None)

        else:
            self.activate_idx(None)

        event.accept()

    def mouseMoveEvent(self, event):
        if self._left_click:
            point = (event.x() - self._scroll_contents.geometry().x(), event.y() - self._scroll_contents.geometry().y())

            col = point[0] // self._pl_wid
            row = point[1] // self._pl_wid

            if col <= self._args.stab_column:
                idx = self._args.stab_column * row + col

                if idx < len(self._args.stab_ucells) - 1:
                    self._args.stab_ucells.pop(self._current_idx)
                    self._current_idx = idx

                    self._args.stab_ucells.insert(idx, None)

            self._fetched_cell.setGeometry(point[0] - self._pl_wid / 2, point[1] - self._pl_wid / 2, self._pl_wid, self._pl_wid)

            self.update()
            event.accept()

        elif self._start_hig != None:
            self._scroll_bar.setValue(self._start_hig - event.y())

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._start_hig = None

        if self._left_click:
            self._args.stab_ucells[self._current_idx] = self._fetched_cell
            self._fetched_cell = None

            self._left_click = False

            self.update()
            event.accept()

        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = (event.x() - self._scroll_contents.geometry().x(), event.y() - self._scroll_contents.geometry().y())

            col = point[0] // self._pl_wid
            row = point[1] // self._pl_wid

            if col <= self._args.stab_column:
                idx = self._args.stab_column * row + col

                if idx < len(self._args.stab_ucells):
                    self.activate_idx(idx)

                    if idx == len(self._args.stab_ucells) - 1:
                        self.attach_set()
                    
                    else:
                        self.import_set()

                else:
                    self.activate_idx(None)

            else:
                self.activate_idx(None)

            event.accept()

        else:
            event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def initialize(self):
        """
        Initialize Depot from self._args.stab_ucells list.
        """

        unit_cells = []

        for cset in self._args.stab_ucells:
            unit_cell = UnitCell(self._scroll_contents, self._args, cset[0], cset[1], cset[2])
            unit_cells.append(unit_cell)

            self._scroll_grid_layout.addWidget(unit_cell)

        empty_cell = UnitCell(self._scroll_contents, self._args, [None, None, None, None, None], "", "")
        unit_cells.append(empty_cell)

        self._scroll_grid_layout.addWidget(empty_cell)

        self._args.stab_ucells = unit_cells

        self._current_idx = None

    def create_menu(self):
        """
        Create a right clicked menu.
        """

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

        self._menu = QMenu(self)

        self._action_import = QAction(self)
        self._action_import.triggered.connect(self.import_set)
        self._menu.addAction(self._action_import)

        self._action_export = QAction(self)
        self._menu.addAction(self._action_export)

        self._action_delete = QAction(self)
        self._action_delete.triggered.connect(self.delete_set)
        self._menu.addAction(self._action_delete)

        self._action_detail = QAction(self)
        self._action_detail.triggered.connect(self._info.show)
        self._menu.addAction(self._action_detail)

        self._action_attach = QAction(self)
        self._action_attach.triggered.connect(self.attach_set)
        self._menu.addAction(self._action_attach)

    def show_menu(self):
        """
        Show the right clicked menu.
        """

        if self._current_idx == None:
            self._action_import.setDisabled(True)
            self._action_export.setDisabled(True)
            self._action_delete.setDisabled(True)
            self._action_detail.setDisabled(True)
            self._action_attach.setDisabled(True)

        elif self._current_idx == len(self._args.stab_ucells) - 1:
            self._action_import.setDisabled(True)
            self._action_export.setDisabled(True)
            self._action_delete.setDisabled(True)
            self._action_detail.setDisabled(True)
            self._action_attach.setDisabled(False)

        else:
            self._action_import.setDisabled(False)
            self._action_export.setDisabled(False)
            self._action_delete.setDisabled(False)
            self._action_detail.setDisabled(False)
            self._action_attach.setDisabled(True)

        self._menu.exec_(QCursor.pos())

    def activate_idx(self, idx, update=True):
        """
        Activate current idx unit cell.
        """

        if self._current_idx != None:
            self._args.stab_ucells[self._current_idx].activated = False
            self._args.stab_ucells[self._current_idx].update()

        self._current_idx = idx

        if self._current_idx != None:
            self._current_idx = self._current_idx if self._current_idx > 0 else 0
            self._current_idx = self._current_idx if self._current_idx < len(self._args.stab_ucells) else len(self._args.stab_ucells) - 1

        if self._current_idx != None and isinstance(self._args.stab_ucells[self._current_idx], UnitCell):
            self._args.stab_ucells[self._current_idx].activated = True
            self._args.stab_ucells[self._current_idx].update()

            if update:
                upp_pos = self._scroll_contents.geometry().y() + self._args.stab_ucells[self._current_idx].geometry().y()
                low_pos = self._scroll_contents.geometry().y() + self._args.stab_ucells[self._current_idx].geometry().y() + self._args.stab_ucells[self._current_idx].geometry().height()

                if upp_pos <= 0:
                    self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].geometry().y())

                elif low_pos >= self._scroll_area.geometry().height():
                    self._scroll_bar.setValue(self._args.stab_ucells[self._current_idx].geometry().y() + self._pl_wid - self._scroll_area.geometry().height())

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

        stab_column = self._args.stab_column

        if ratio > 1:
            stab_column -= 1

        elif ratio < 1:
            stab_column += 1

        self._args.modify_settings("stab_column", stab_column)

        self.update()

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

        elif self._current_idx == len(self._args.stab_ucells) - 1:
            self.attach_set()

        elif self._current_idx < len(self._args.stab_ucells) - 1:
            self.import_set()

    def delete_set(self):
        """
        Delete current color set from depot.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        self._args.stab_ucells[self._current_idx].close()
        self._args.stab_ucells.pop(self._current_idx)

        self._args.stab_ucells[self._current_idx].activated = True
        self.update()

    def attach_set(self):
        """
        Attach current color set into depot.
        """

        if not self.isVisible():
            return

        hsv_set = (self._args.sys_color_set[0].hsv, self._args.sys_color_set[1].hsv, self._args.sys_color_set[2].hsv, self._args.sys_color_set[3].hsv, self._args.sys_color_set[4].hsv)
        
        unit_cell = UnitCell(self._scroll_contents, self._args, hsv_set, self._args.hm_rule, "")
        self._scroll_grid_layout.addWidget(unit_cell)

        empty_cell = self._args.stab_ucells[len(self._args.stab_ucells) - 1]
        empty_cell.activated = False

        self._args.stab_ucells[len(self._args.stab_ucells) - 1] = unit_cell
        self._args.stab_ucells.append(empty_cell)

        self.activate_idx(len(self._args.stab_ucells) - 2, update=False)
        self.update()

    def import_set(self):
        """
        Import current color set into color wheel.
        """

        if not self.isVisible():
            return

        if self._current_idx == None or self._current_idx > len(self._args.stab_ucells) - 2:
            return

        self._args.sys_color_set.import_color_set(self._args.stab_ucells[self._current_idx].color_set)
        self._args.hm_rule = self._args.stab_ucells[self._current_idx].hm_rule

        self.ps_update.emit(True)

    def clean_up(self):
        """
        Delete all unit cells except empty cell.
        """

        for unit_cell in self._args.stab_ucells[:-1]:
            if isinstance(unit_cell, UnitCell):
                unit_cell.close()

        self._args.stab_ucells = self._args.stab_ucells[-1:]
        self._args.stab_ucells[0].activated = False
        self._current_idx = None

        self.update()

    def update_all(self):
        """
        Update all unit cells and self.
        """

        for unit_cell in self._args.stab_ucells:
            if isinstance(unit_cell, UnitCell):
                unit_cell.update()

        self.update()

    def closeEvent(self, event):
        """
        Actions before close Depot.
        """

        stab_ucells = []

        for unit_cell in self._args.stab_ucells[:-1]:
            if isinstance(unit_cell, UnitCell):
                hsv_set = (
                    unit_cell.color_set[0].hsv,
                    unit_cell.color_set[1].hsv,
                    unit_cell.color_set[2].hsv,
                    unit_cell.color_set[3].hsv,
                    unit_cell.color_set[4].hsv,
                )

                stab_ucells.append((hsv_set, unit_cell.hm_rule, unit_cell.desc))

        self._args.stab_ucells = tuple(stab_ucells)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self._action_import.setText(self._action_descs[0])
        self._action_export.setText(self._action_descs[1])
        self._action_delete.setText(self._action_descs[2])
        self._action_detail.setText(self._action_descs[3])
        self._action_attach.setText(self._action_descs[4])

        self._info._func_tr_()
        self._info.update_text()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Depot", "Import"),
            _translate("Depot", "Export"),
            _translate("Depot", "Delete"),
            _translate("Depot", "Detail"),
            _translate("Depot", "Attach"),
        )
