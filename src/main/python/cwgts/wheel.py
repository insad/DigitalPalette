# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QRadialGradient, QLinearGradient
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QCoreApplication
from clibs.create import Create
from clibs.color import Color
from clibs import info as dpinfo
from clibs.trans2d import get_outer_box, rotate_point_center, get_theta_center
import numpy as np
import json
import os
import time


class Wheel(QWidget):
    """
    Wheel object based on QWidget. Init a color wheel in work space.

    selected_color_set is a pyqt signal contains current color set.
    """

    selected_color_0 = pyqtSignal(np.ndarray)
    selected_color_1 = pyqtSignal(np.ndarray)
    selected_color_2 = pyqtSignal(np.ndarray)
    selected_color_3 = pyqtSignal(np.ndarray)
    selected_color_4 = pyqtSignal(np.ndarray)

    selected_acitve_0 = pyqtSignal(bool)
    selected_acitve_1 = pyqtSignal(bool)
    selected_acitve_2 = pyqtSignal(bool)
    selected_acitve_3 = pyqtSignal(bool)
    selected_acitve_4 = pyqtSignal(bool)

    selected_hm_rule = pyqtSignal(str)

    def __init__(self, settings):
        """
        Init the color wheel.

        Parameters:
          setting - dict. setting environment. {"h_range": h_range, "s_range": s_range, "v_range": v_range}.
        """

        super().__init__()

        # loading settings.
        # hm rule is not allowed to reload.
        self.reload_settings(settings)
        self._env_hm_rule = settings[20]

        self._create = Create(self._pr_h_range, self._pr_s_range, self._pr_v_range)
        self._create.create(self._env_hm_rule)

        self._emit_color = False       # emit selected_color_0 or 1, 2, 3, 4
        self._emit_other_color = False # emit other selected_color_0 or 1, 2, 3, 4
        self._receive_color = True     # receive selected_color_0 or 1, 2, 3, 4
        self._emit_activate = False    # emit activate state to all cube squares.

        self._active_color_idx = 0  # the index of activated color for modify. 
        self._color_actived = False # for mouse press, move and release events.
        self._wheel_actived = False # for mouse press, move on wheel.
        self._bar_1_actived = False # for mouse press, move on bar 1.
        self._bar_2_actived = False # for mouse press, move on bar 2.

        self._func_tr_()

    def reload_settings(self, settings):
        self._pr_h_range = settings[0]
        self._pr_s_range = settings[1]
        self._pr_v_range = settings[2]

        self._env_radius = settings[3]
        self._env_color_radius = settings[4]
        self._env_press_move = settings[22]
        self._env_at_color = settings[12]
        self._env_ia_color = settings[13]
        self._env_bar_widratio = settings[7]
        self._env_vb_color = settings[14]

    @property
    def color_set(self):
        return self._create.color_set

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()
        self._center = np.array((wid / 2.0, hig / 2.0), dtype=int)
        self._radius = min(wid, hig) * self._env_radius / 2

        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # color wheel.
        wheel_box = get_outer_box(self._center, self._radius)
        painter.setPen(QPen(Qt.NoPen))
        cgrad = QConicalGradient(*self._center, 0)
        cgrad.setColorAt(0.00000, QColor(255, 0  , 0  ))
        cgrad.setColorAt(0.16667, QColor(255, 0  , 255))
        cgrad.setColorAt(0.33333, QColor(0  , 0  , 255))
        cgrad.setColorAt(0.50000, QColor(0  , 255, 255))
        cgrad.setColorAt(0.66667, QColor(0  , 255, 0  ))
        cgrad.setColorAt(0.83333, QColor(255, 255, 0  ))
        cgrad.setColorAt(1.00000, QColor(255, 0  , 0  ))
        painter.setBrush(cgrad)
        painter.drawEllipse(*wheel_box)

        rgrad = QRadialGradient(*self._center, self._radius)
        rgrad.setColorAt(0.0, Qt.white)
        rgrad.setColorAt(1.0, Qt.transparent)
        painter.setBrush(rgrad)
        painter.drawEllipse(*wheel_box)

        # color set.
        self._color_centers = []
        self._color_radius = min(wid, hig) * self._env_color_radius / 2
        for idx in range(5):
            color = self._create.color_set[idx]
            color_center = np.array([color.s * self._radius, 0]) + self._center
            color_center = rotate_point_center(self._center, color_center, color.h)

            self._color_centers.append(color_center)

        idx_seq = list(range(5))
        idx_seq = idx_seq[self._active_color_idx + 1:] + idx_seq[: self._active_color_idx + 1]
        for idx in idx_seq:
            color = self._create.color_set[idx]
            color_center = self._color_centers[idx]
            color_box = get_outer_box(color_center, self._color_radius)

            if idx == self._active_color_idx:
                painter.setPen(QPen(QColor(*self._env_at_color), 3))
            else:
                painter.setPen(QPen(QColor(*self._env_ia_color), 2))
            painter.drawLine(QPoint(*self._center), QPoint(*color_center))
            painter.setBrush(QColor(*color.rgb))
            painter.drawEllipse(*color_box)

        # bars.
        current_color = Color(self._create.color_set[self._active_color_idx])
        current_v = current_color.v
        current_color.v = 1

        re_wid = wid * (1 - self._env_radius) / 2 * self._env_bar_widratio
        re_wid = self._color_radius * 3 if self._color_radius * 3 < re_wid else re_wid

        bar_1_center = ((wid - self._radius * 2) / 4, hig / 2)
        self._bar_1_box = (bar_1_center[0] - re_wid / 2, bar_1_center[1] - hig * self._env_bar_widratio / 2, re_wid, hig * self._env_bar_widratio)
        painter.setPen(QPen(QColor(*self._env_vb_color), 2))
        lgrad = QLinearGradient(self._bar_1_box[0], self._bar_1_box[1], self._bar_1_box[0], self._bar_1_box[3])
        lgrad.setColorAt(1.0, Qt.white)
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_1_box)

        self._cir_1_center = (bar_1_center[0], self._bar_1_box[1] + self._bar_1_box[3] * current_v)
        cir_1_box = get_outer_box(self._cir_1_center, self._color_radius)
        painter.setPen(QPen(QColor(*self._env_vb_color), 2))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_1_box)

        bar_2_center = (wid - (wid - self._radius * 2) / 4, hig / 2)
        self._bar_2_box = (bar_2_center[0] - re_wid / 2, bar_2_center[1] - hig * self._env_bar_widratio / 2, re_wid, hig * self._env_bar_widratio)
        painter.setPen(QPen(QColor(*self._env_vb_color), 2))
        lgrad = QLinearGradient(self._bar_2_box[0], self._bar_2_box[1], self._bar_2_box[0], self._bar_2_box[3])
        lgrad.setColorAt(1.0, QColor(*current_color.rgb))
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_2_box)

        self._cir_2_center = (bar_2_center[0], self._bar_2_box[1] + self._bar_2_box[3] * current_v)
        cir_2_box = get_outer_box(self._cir_2_center, self._color_radius)
        painter.setPen(QPen(QColor(*self._env_vb_color), 2))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_2_box)

        painter.end()

        if self._emit_color:
            for i in range(5):
                selected_color = getattr(self, "selected_color_{}".format(i))
                selected_color.emit(self._create.color_set[i].hsv)
            # self._emit_color can only closed by mouse release event.
            # self._emit_color = False
            self._emit_other_color = False

        if self._emit_other_color:
            for i in range(5):
                if i != self._active_color_idx:
                    selected_color = getattr(self, "selected_color_{}".format(i))
                    selected_color.emit(self._create.color_set[i].hsv)
            self._emit_other_color = False

        if self._color_actived or self._emit_activate:
            for i in range(5):
                selected_acitve = getattr(self, "selected_acitve_{}".format(i))
                if i == self._active_color_idx:
                    selected_acitve.emit(True)
                else:
                    selected_acitve.emit(False)
            self._emit_activate = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = np.array((event.x(), event.y()))

            self._receive_color = False
            self._emit_color = True
            self._emit_other_color = False
            self._emit_activate = True
            self._color_actived = True

            if np.linalg.norm(point - self._center) < self._radius:
                aly_accepted = True
                self._create.backup()

                for idx in range(5):
                    if np.linalg.norm(point - self._color_centers[idx]) < self._color_radius:
                        self._active_color_idx = idx
                        self._wheel_actived = True
                        aly_accepted = False
                        event.accept()
                        self.update()
                        break

                if aly_accepted and self._env_press_move:
                    color = Color(self._create.color_set[self._active_color_idx])
                    color.s = np.linalg.norm(point - self._center) / self._radius
                    color.h = get_theta_center(self._center, point)
                    self._create.modify(self._env_hm_rule, self._active_color_idx, color)
                    self._wheel_actived = True
                    event.accept()
                    self.update()

            elif self._bar_1_box[0] < point[0] < self._bar_1_box[0] + self._bar_1_box[2] and self._bar_1_box[1] < point[1] < self._bar_1_box[1] + self._bar_1_box[3]:
                v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
                v = 1.0 if v > 1.0 else v
                v = 0.0 if v < 0.0 else v
                self._create.color_set[self._active_color_idx].v = v
                self._bar_1_actived = True
                event.accept()
                self.update()

            elif self._bar_2_box[0] < point[0] < self._bar_2_box[0] + self._bar_2_box[2] and self._bar_2_box[1] < point[1] < self._bar_2_box[1] + self._bar_2_box[3]:
                v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
                v = 1.0 if v > 1.0 else v
                v = 0.0 if v < 0.0 else v
                self._create.color_set[self._active_color_idx].v = v
                self._bar_2_actived = True
                event.accept()
                self.update()

            else:
                event.ignore()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._color_actived:
            point = np.array((event.x(), event.y()))

            if self._wheel_actived:
                color = Color(self._create.color_set[self._active_color_idx])
                color.overflow_s(np.linalg.norm(point - self._center) / self._radius)
                color.h = get_theta_center(self._center, point)
                self._create.recover()
                self._create.modify(self._env_hm_rule, self._active_color_idx, color)
                event.accept()
                self.update()

            elif self._bar_1_actived:
                v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
                v = 1.0 if v > 1.0 else v
                v = 0.0 if v < 0.0 else v
                self._create.color_set[self._active_color_idx].v = v
                event.accept()
                self.update()

            elif self._bar_2_actived:
                v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
                v = 1.0 if v > 1.0 else v
                v = 0.0 if v < 0.0 else v
                self._create.color_set[self._active_color_idx].v = v
                event.accept()
                self.update()

            else:
                event.ignore()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._receive_color = True
        self._emit_color = False
        self._emit_other_color = False
        self._emit_activate = False
        self._color_actived = False
        self._wheel_actived = False
        self._bar_1_actived = False
        self._bar_2_actived = False


    # ===== ===== ===== slot functions ===== ===== =====

    def slot_modify_hm_rule(self, hm_rule):
        """
        Slot func. Change current harmony rule.
        """

        def _func_(value):
            if hm_rule != self._env_hm_rule:
                self._env_hm_rule = hm_rule
                self._create.create(self._env_hm_rule)

                self._emit_color = True
                self._emit_other_color = False
                self._emit_activate = True
                self.update()
        return _func_

    def slot_modify_color(self, index):
        """
        Slot func. Change the selected color (index) in created color set. 
        """

        def _func_(color):
            if self._receive_color and not self._create.color_set[index].hsv_eq(color, acr=1E-3):
                self._create.modify(self._env_hm_rule, index, Color(color, ctp="hsv"))
                self._active_color_idx = int(index)

                self._emit_color = False
                self._emit_other_color = True
                self._emit_activate = True
                self.update()
        return _func_

    def slot_recreate(self):
        """
        Slot func. Recreate color set.
        """

        self._create = Create(self._pr_h_range, self._pr_s_range, self._pr_v_range)
        self._create.create(self._env_hm_rule)
        self._emit_color = True
        self.update()

    def slot_modify_activate_index(self, index):
        """
        Slot func. Change current activated color index by cube square.
        There are five squares and only on state would be True.
        It can only receive when color not activated (self._color_actived = False), i.e. not in mouse event.
        """

        def _func_(state):
            if not self._color_actived and state and index != self._active_color_idx:
                self._active_color_idx = int(index)

                self._emit_color = False
                self._emit_other_color = False
                self._emit_activate = True # set True to keep only one in cube squares activated.
                self.update()
        return _func_

    def slot_export(self):
        default_name = "{}".format(time.strftime("digipale_%Y_%m_%d", time.localtime()))
        default_path = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette", "MyColors"))
        if not os.path.isdir(default_path):
            os.makedirs(default_path)

        cb_filter = "DigitalPalette Json File (*.json);; Plain Text (*.txt);; Swatch File (*.aco)"
        cb_file = QFileDialog.getSaveFileName(None, self._dia_descs[0],  os.sep.join((default_path, default_name)), filter=cb_filter)

        if cb_file[0]:
            if cb_file[0].split(".")[-1].lower() == "json":
                color_dict = {"version": dpinfo.current_version(), "harmony_rule": self._env_hm_rule}
                color_dict.update(self._create.export_color_set())

                with open(cb_file[0], "w") as f:
                    json.dump(color_dict, f, indent=4)
            
            elif cb_file[0].split(".")[-1].lower() == "txt":
                with open(cb_file[0], "w") as f:
                    f.write("# DigitalPalette Color Export.\n")
                    f.write("# Version: {}.\n".format(dpinfo.current_version()))
                    f.write("# Harmony Rule: {}.\n".format(self._env_hm_rule))
                    f.write(self._create.export_text())                    

            elif cb_file[0].split(".")[-1].lower() == "aco":
                color_swatch = self._create.export_swatch()
                with open(cb_file[0], "wb") as f:
                    f.write(color_swatch)

            else:
                QMessageBox.warning(self, self._err_descs[0], self._err_descs[9].format(cb_file[0]))

    def slot_import(self):
        interface_cmp = True
        if not self.isVisible():
            interface_cmp = False
            QMessageBox.warning(self, self._err_descs[0], self._err_descs[8])

        cb_file = [None,]
        if interface_cmp:
            default_path = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette", "MyColors"))
            if not os.path.isdir(default_path):
                os.makedirs(default_path)

            cb_filter = "DigitalPalette Json File (*.json)"
            cb_file = QFileDialog.getOpenFileName(None, self._dia_descs[1], default_path, filter=cb_filter)
    
        if cb_file[0]:
            file_cmp = True
            color_dict = {}
            with open(cb_file[0], "r") as f:
                try:
                    color_dict = json.load(f)
                except:
                    QMessageBox.warning(self, self._err_descs[0], self._err_descs[10])
                    file_cmp = False
                
                if not isinstance(color_dict, dict):
                    QMessageBox.warning(self, self._err_descs[0], self._err_descs[10])
                    file_cmp = False

            color_cmp = False
            if file_cmp:
                if "version" in color_dict:
                    if dpinfo.if_version_compatible(color_dict["version"]):
                        err = self._create.import_color_set(color_dict)
                        if err:
                            QMessageBox.warning(self, self._err_descs[0], self._err_descs[err[0]].format(*err[1]))
                        else:
                            color_cmp = True
                    else:
                        QMessageBox.warning(self, self._err_descs[0], self._err_descs[4].format(color_dict["version"]))
                else:
                    QMessageBox.warning(self, self._err_descs[0], self._err_descs[5].format(os.path.basename(cb_file[0])))

            if color_cmp:
                if "harmony_rule" in color_dict:
                    if color_dict["harmony_rule"] in ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom"):
                        self._env_hm_rule = color_dict["harmony_rule"]
                    else:
                        self._env_hm_rule = "custom"
                        QMessageBox.warning(self, self._err_descs[0], self._err_descs[6].format(color_dict["harmony_rule"]))
                else:
                    self._env_hm_rule = "custom"
                    QMessageBox.warning(self, self._err_descs[0], self._err_descs[7])

                self._emit_color = True
                self.selected_hm_rule.emit(self._env_hm_rule)
                self.update()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._err_descs = (
            _translate("Wheel", "Error"),
            _translate("Wheel", "Color {0} doesn't exist in data file."),
            _translate("Wheel", "The HSV tag of color {0} doesn't exist in data file."),
            _translate("Wheel", "Color {0} with HSV value is invalid: {1}."),
            _translate("Wheel", "Version is not compatible for data file: {0}."),
            _translate("Wheel", "Unknown version of data file {0}."),
            _translate("Wheel", "Harmony rule is invalid: {0}. Using custom instead."),
            _translate("Wheel", "Harmony rule doesn't exist in data file. Use custom instead."),
            _translate("Wheel", "Data files can only be imported in color wheel interface."),
            _translate("Wheel", "Unknown data file extension: {0}."),
            _translate("Wheel", "Data file is broken."),
        )

        self._dia_descs = (
            _translate("Wheel", "Export"),
            _translate("Wheel", "Import"),
        )
