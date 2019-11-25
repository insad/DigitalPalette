# -*- coding: utf-8 -*-

import os
import time
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QCoreApplication, QSize
from clibs.color import Color


class Operation(QWidget):
    """
    Operation object based on QWidget. Init a operation in operation.
    """

    ps_create = pyqtSignal(bool)
    ps_locate = pyqtSignal(bool)
    ps_update = pyqtSignal(bool)

    def __init__(self, args):
        """
        Init operation.
        """

        super().__init__()

        # load args.
        self._args = args

        # load translations.
        self._func_tr_()

        # init qt args.
        operation_grid_layout = QGridLayout(self)
        operation_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setWidgetResizable(True)
        operation_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        self.import_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.import_btn, 0, 1, 1, 1)
        self.import_btn.clicked.connect(self.exec_import)

        self.export_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.export_btn, 1, 1, 1, 1)
        self.export_btn.clicked.connect(self.exec_export)

        self.create_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.create_btn, 2, 1, 1, 1)
        self.create_btn.clicked.connect(self.exec_create)

        self.locate_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.locate_btn, 3, 1, 1, 1)
        self.locate_btn.clicked.connect(self.exec_locate)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 4, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 4, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 4, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(180, 90)

    def exec_import(self, value):
        """
        Exec import operation.
        """

        cb_filter = "Json File (*.json)"
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[0], self._args.usr_color, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        color_dict = {}

        with open(cb_file[0], "r") as f:
            try:
                color_dict = json.load(f)

            except:
                QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[1])
                file_cmp = False
                return

            if not isinstance(color_dict, dict):
                QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[2])
                return

        if "version" in color_dict:
            if not self._args.check_version(color_dict["version"]):
                QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[3])
                return

        else:
            QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[4])
            return

        color_set = []

        for i in range(5):
            if "color_{}".format(i) in color_dict:
                if "hsv" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hsv"]
                        color_set.append(Color(hsv, tp="hsv", overflow=self._args.sys_color_set.get_overflow()))

                    except:
                        QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[5])
                        return

                else:
                    QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[6])
                    return

            else:
                QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[7])
                return

        if "harmony_rule" in color_dict:
            if color_dict["harmony_rule"] in self._args.global_hm_rules:
                self._args.hm_rule = color_dict["harmony_rule"]
                self._args.sys_color_set.import_color_set(color_set)

            else:
                QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[8])
                return

        else:
            QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[9])
            return

        self.ps_update.emit(True)

    def exec_export(self, value):
        """
        Exec export operation.
        """

        name = "{}".format(time.strftime("digipale_%Y_%m_%d.json", time.localtime()))

        cb_filter = "Json File (*.json);; Plain Text (*.txt);; Swatch File (*.aco)"
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[1], os.sep.join((self._args.usr_color, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        if cb_file[0].split(".")[-1].lower() == "json":
            color_dict = {"version": self._args.info_version, "harmony_rule": self._args.hm_rule}
            color_dict.update(self._args.sys_color_set.export_dict())

            with open(cb_file[0], "w") as f:
                json.dump(color_dict, f, indent=4)

        elif cb_file[0].split(".")[-1].lower() == "txt":
            with open(cb_file[0], "w") as f:
                f.write("# DigitalPalette Color Export.\n")
                f.write("# Version: {}.\n".format(self._args.info_version))
                f.write("# Harmony Rule: {}.\n".format(self._args.hm_rule))
                f.write(self._args.sys_color_set.export_text())                    

        elif cb_file[0].split(".")[-1].lower() == "aco":
            color_swatch = self._args.sys_color_set.export_swatch()
            with open(cb_file[0], "wb") as f:
                f.write(color_swatch)

        else:
            QMessageBox.warning(self, self._operation_errs[0], self._operation_errs[10])


    def exec_create(self, value):
        """
        Exec create operation.
        """

        self.ps_create.emit(True)

    def exec_locate(self, value):
        """
        Exec loacate operation.
        """

        self.ps_locate.emit(True)

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.import_btn.setText(self._operation_descs[0])
        self.export_btn.setText(self._operation_descs[1])
        self.create_btn.setText(self._operation_descs[2])
        self.locate_btn.setText(self._operation_descs[3])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._operation_descs = (
            _translate("Operation", "Import"),
            _translate("Operation", "Export"),
            _translate("Operation", "Create"),
            _translate("Operation", "Locate"),
        )

        self._operation_errs = (
            _translate("Operation", "Error"),
            _translate("Operation", "Import color file error. Color file is broken."),
            _translate("Operation", "Import color format error. Data is not in dict type."),
            _translate("Operation", "Import color version error. Version does not match."),
            _translate("Operation", "Import color version error. Version does not exist."),
            _translate("Operation", "Import color set error. Color set is broken."),
            _translate("Operation", "Import color set error. HSV tags do not exist."),
            _translate("Operation", "Import color set error. Color tags do not exist."),
            _translate("Operation", "Import harmony rule error. Rule does not match."),
            _translate("Operation", "Import harmony rule error. Rule does not exist."),
            _translate("Operation", "Export Color file error. Extension does not match."),
        )
