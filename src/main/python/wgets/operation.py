# -*- coding: utf-8 -*-

import os
import time
import json
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QSize
from clibs.export import export_list, export_text, export_swatch
from clibs.color import Color


class Operation(QWidget):
    """
    Operation object based on QWidget. Init a operation in operation.
    """

    ps_create = pyqtSignal(bool)
    ps_locate = pyqtSignal(bool)
    ps_update = pyqtSignal(bool)
    ps_attach = pyqtSignal(bool)
    ps_opened = pyqtSignal(bool)

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
        operation_grid_layout = QGridLayout(self)
        operation_grid_layout.setContentsMargins(1, 1, 1, 1)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Box)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        operation_grid_layout.addWidget(scroll_area)

        scroll_contents = QWidget()
        scroll_grid_layout = QGridLayout(scroll_contents)
        scroll_grid_layout.setContentsMargins(8, 8, 8, 8)
        scroll_grid_layout.setHorizontalSpacing(8)
        scroll_grid_layout.setVerticalSpacing(12)
        scroll_area.setWidget(scroll_contents)

        self.open_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.open_btn, 0, 1, 1, 1)
        self.open_btn.clicked.connect(self.exec_open)

        self.save_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.save_btn, 1, 1, 1, 1)
        self.save_btn.clicked.connect(self.exec_save)

        self.import_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.import_btn, 2, 1, 1, 1)
        self.import_btn.clicked.connect(self.exec_import)

        self.export_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.export_btn, 3, 1, 1, 1)
        self.export_btn.clicked.connect(self.exec_export)

        self.create_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.create_btn, 4, 1, 1, 1)
        self.create_btn.clicked.connect(self.exec_create)

        self.locate_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.locate_btn, 5, 1, 1, 1)
        self.locate_btn.clicked.connect(self.exec_locate)

        self.attach_btn = QPushButton(scroll_contents)
        scroll_grid_layout.addWidget(self.attach_btn, 6, 1, 1, 1)
        self.attach_btn.clicked.connect(self.exec_attach)

        spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_grid_layout.addItem(spacer, 7, 1, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 7, 0, 1, 1)
        spacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        scroll_grid_layout.addItem(spacer, 7, 2, 1, 1)

        self.update_text()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def sizeHint(self):
        return QSize(180, 160)

    def exec_open(self, value):
        """
        Exec open operation.
        """

        cb_filter = "{} (*.json)".format(self._file_descs[0])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[0], self._args.usr_color, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        color_dict = {}

        with open(cb_file[0], "r", encoding='utf-8') as f:
            try:
                color_dict = json.load(f)

            except Exception as err:
                self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                return

            if not isinstance(color_dict, dict):
                self.warning(self._operation_errs[2])
                return

        if "version" in color_dict:
            if not self._args.check_version(color_dict["version"]):
                self.warning(self._operation_errs[3])
                return

        else:
            self.warning(self._operation_errs[4])
            return

        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "depot":
                color_dict = color_dict["palettes"]

            elif color_dict["type"] == "set":
                self.warning(self._operation_errs[15])
                return

            else:
                self.warning(self._operation_errs[11])
                return

        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return

        color_list = []
        finished_errs = []

        try:
            for color in color_dict:
                hsv_set = []

                try:
                    for i in range(5):
                        hsv_set.append(tuple(Color.fmt_hsv(color["color_{}".format(i)]["hsv"]).tolist()))

                    if color["rule"] in self._args.global_hm_rules:
                        color_list.append((tuple(hsv_set), color["rule"], str(color["desc"])))

                    else:
                        finished_errs.append("unknown rule: {}.".format(color["rule"]))

                except Exception as err:
                    finished_errs.append(str(err))

        except Exception as err:
            self.warning(self._operation_errs[13] + "\n{}\n{}".format(self._operation_errs[17], err))
            return

        if finished_errs:
            self.warning(self._operation_errs[14] + "\n{}\n{}".format(self._operation_errs[17], "; ".join(finished_errs)))

        for unit_cell in self._args.stab_ucells:
            if hasattr(unit_cell, "close"):
                unit_cell.close()

        self._args.stab_ucells = tuple(color_list)
        self.ps_opened.emit(True)

    def exec_save(self, value):
        """
        Exec save operation.
        """

        name = "{}".format(time.strftime("DigiPale_Depot_%Y_%m_%d.json", time.localtime()))

        cb_filter = "{} (*.json);; {} (*.txt);; {} (*.aco)".format(self._file_descs[0], self._file_descs[1], self._file_descs[2])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[1], os.sep.join((self._args.usr_color, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        # load color set from unit cells, which is different from export.
        color_list = []

        for unit_cell in self._args.stab_ucells[:-1]:
            if unit_cell != None:
                color_list.append((unit_cell.color_set, unit_cell.hm_rule, unit_cell.desc))

        # process start.
        if cb_file[0].split(".")[-1].lower() == "json":
            color_dict = {"version": self._args.info_version, "type": "depot"}
            color_dict["palettes"] = export_list(color_list)

            with open(cb_file[0], "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4)

        elif cb_file[0].split(".")[-1].lower() == "txt":
            with open(cb_file[0], "w") as f:
                f.write("# DigitalPalette Color Export\n")
                f.write("# Version: {}\n\n".format(self._args.info_version))
                f.write(export_text(color_list))

        elif cb_file[0].split(".")[-1].lower() == "aco":
            with open(cb_file[0], "wb") as f:
                f.write(export_swatch(color_list))

        else:
            self.warning(self._operation_errs[10])

    def exec_import(self, value):
        """
        Exec import operation.
        """

        cb_filter = "{} (*.json)".format(self._file_descs[0])
        cb_file = QFileDialog.getOpenFileName(None, self._operation_descs[0], self._args.usr_color, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        color_dict = {}

        with open(cb_file[0], "r", encoding='utf-8') as f:
            try:
                color_dict = json.load(f)

            except Exception as err:
                self.warning(self._operation_errs[1] + "\n{}\n{}".format(self._operation_errs[17], err))
                return

            if not isinstance(color_dict, dict):
                self.warning(self._operation_errs[2])
                return

        if "version" in color_dict:
            if not self._args.check_version(color_dict["version"]):
                self.warning(self._operation_errs[3])
                return

        else:
            self.warning(self._operation_errs[4])
            return

        if "type" in color_dict and "palettes" in color_dict:
            if color_dict["type"] == "set":
                color_dict = color_dict["palettes"][0]

            elif color_dict["type"] == "depot":
                self.warning(self._operation_errs[16])
                return

            else:
                self.warning(self._operation_errs[11])
                return

        else:
            self.warning(self._operation_errs[12] + "\n{}\n{}".format(self._operation_errs[17], "type; palettes"))
            return

        color_set = []

        for i in range(5):
            if "color_{}".format(i) in color_dict:
                if "hsv" in color_dict["color_{}".format(i)]:
                    try:
                        hsv = color_dict["color_{}".format(i)]["hsv"]
                        color_set.append(Color(hsv, tp="hsv", overflow=self._args.sys_color_set.get_overflow()))

                    except Exception as err:
                        self.warning(self._operation_errs[5] + "\n{}\n{}".format(self._operation_errs[17], err))
                        return

                else:
                    self.warning(self._operation_errs[6] + "\n{}\n{}".format(self._operation_errs[17], "hsv"))
                    return

            else:
                self.warning(self._operation_errs[7] + "\n{}\n{}".format(self._operation_errs[17], "color_{}".format(i)))
                return

        if "rule" in color_dict:
            if color_dict["rule"] in self._args.global_hm_rules:
                self._args.hm_rule = color_dict["rule"]
                self._args.sys_color_set.import_color_set(color_set)

            else:
                self.warning(self._operation_errs[8] + "\n{}\n{}".format(self._operation_errs[17], color_dict["rule"]))
                return

        else:
            self.warning(self._operation_errs[9] + "\n{}\n{}".format(self._operation_errs[17], "rule"))
            return

        self.ps_update.emit(True)

    def exec_export(self, value):
        """
        Exec export operation.
        """

        name = "{}".format(time.strftime("DigiPale_Set_%Y_%m_%d.json", time.localtime()))

        cb_filter = "{} (*.json);; {} (*.txt);; {} (*.aco)".format(self._file_descs[0], self._file_descs[1], self._file_descs[2])
        cb_file = QFileDialog.getSaveFileName(None, self._operation_descs[1], os.sep.join((self._args.usr_color, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_color = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        # load color set from sys or depot, which is different from save.
        color_set = None
        hm_rule = None
        desc = ""

        if isinstance(value, bool):
            color_set = self._args.sys_color_set
            hm_rule = self._args.hm_rule
            desc = "#Name: DigiPale Color Set"

        else:
            color_set = self._args.stab_ucells[value].color_set
            hm_rule = self._args.stab_ucells[value].hm_rule
            desc = self._args.stab_ucells[value].desc

        # process start.
        if cb_file[0].split(".")[-1].lower() == "json":
            color_dict = {"version": self._args.info_version, "type": "set"}
            color_dict["palettes"] = export_list([(color_set, hm_rule, desc),])

            with open(cb_file[0], "w", encoding='utf-8') as f:
                json.dump(color_dict, f, indent=4)

        elif cb_file[0].split(".")[-1].lower() == "txt":
            with open(cb_file[0], "w") as f:
                f.write("# DigitalPalette Color Export\n")
                f.write("# Version: {}\n\n".format(self._args.info_version))
                f.write(export_text([(color_set, hm_rule, desc),]))

        elif cb_file[0].split(".")[-1].lower() == "aco":
            with open(cb_file[0], "wb") as f:
                f.write(export_swatch([(color_set, hm_rule, desc),]))

        else:
            self.warning(self._operation_errs[10])

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

    def exec_attach(self, value):
        """
        Exec attach operation.
        """

        self.ps_attach.emit(True)

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._operation_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._operation_errs[18], QMessageBox.AcceptRole)
        box.exec_()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def update_text(self):
        self.import_btn.setText(self._operation_descs[0])
        self.export_btn.setText(self._operation_descs[1])
        self.create_btn.setText(self._operation_descs[2])
        self.locate_btn.setText(self._operation_descs[3])
        self.attach_btn.setText(self._operation_descs[4])
        self.open_btn.setText(self._operation_descs[5])
        self.save_btn.setText(self._operation_descs[6])

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._operation_descs = (
            _translate("MainWindow", "Import"),
            _translate("MainWindow", "Export"),
            _translate("MainWindow", "Create"),
            _translate("MainWindow", "Locate"),
            _translate("MainWindow", "Attach"),
            _translate("MainWindow", "Open"),
            _translate("MainWindow", "Save"),
        )

        self._file_descs = (
            _translate("MainWindow", "DigiPale Json File"),
            _translate("MainWindow", "Plain Text File"),
            _translate("MainWindow", "Adobe Swatch File"),
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
            _translate("Operation", "Import color type error. Type does not match."),
            _translate("Operation", "Import color type error. Type does not exist."),
            _translate("Operation", "Import color depot error."),
            _translate("Operation", "Import some color sets into depot error. These color sets are discarded."),
            _translate("Operation", "Import color type error. This is a color set file, please use 'Import'."),
            _translate("Operation", "Import color type error. This is a color depot file, please use 'Open'."),
            _translate("Operation", "Detail:"),
            _translate("Operation", "OK"),
        )
