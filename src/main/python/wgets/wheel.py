# -*- coding: utf-8 -*-

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QSize, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QConicalGradient, QRadialGradient, QLinearGradient
from clibs.transpt import get_outer_box, rotate_point_center, get_theta_center
from clibs.color import Color


class Wheel(QWidget):
    """
    Wheel object based on QWidget. Init a color wheel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_index_changed = pyqtSignal(bool)

    def __init__(self, args):
        """
        Init color wheel.
        """

        super().__init__()

        # load args.
        self._args = args
        self._backup = self._args.sys_color_set.backup()

        # init global args.
        self._pressed_in_wheel = False
        self._pressed_in_bar_1 = False
        self._pressed_in_bar_2 = False

        # init qt args.
        self.setMinimumSize(QSize(300, 200))

    # ---------- ---------- ---------- Paint Funcs ---------- ---------- ---------- #

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()
        self._center = np.array((wid / 2.0, hig / 2.0))
        self._radius = min(wid, hig) * self._args.wheel_ratio / 2

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        # color wheel. hue.
        wheel_box = get_outer_box(self._center, self._radius)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
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

        # color wheel. saturation.
        rgrad = QRadialGradient(*self._center, self._radius)
        rgrad.setColorAt(0.0, Qt.white)
        rgrad.setColorAt(1.0, Qt.transparent)
        painter.setBrush(rgrad)
        painter.drawEllipse(*wheel_box)

        # color set tags.
        self._tag_center = [None] * 5
        self._tag_radius = min(wid, hig) * self._args.s_tag_radius / 2

        idx_seq = list(range(5))
        idx_seq = idx_seq[self._args.sys_activated_idx + 1: ] + idx_seq[: self._args.sys_activated_idx + 1]

        for idx in idx_seq:
            color_center = np.array([self._args.sys_color_set[idx].s * self._radius, 0]) + self._center
            color_center = rotate_point_center(self._center, color_center, self._args.sys_color_set[idx].h)
            self._tag_center[idx] = color_center

            color_box = get_outer_box(color_center, self._tag_radius)
            if idx == self._args.sys_activated_idx:
                painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
            else:
                painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

            painter.drawLine(QPoint(*self._center), QPoint(*color_center))
            painter.setBrush(QColor(*self._args.sys_color_set[idx].rgb))
            painter.drawEllipse(*color_box)

        # bars.
        bar_hsv = self._args.sys_color_set[self._args.sys_activated_idx].hsv
        bar_v = bar_hsv[2]
        bar_rgb = Color.hsv2rgb((bar_hsv[0], bar_hsv[1], 1.0))
        self._v_tag_radius = min(wid, hig) * self._args.v_tag_radius / 2

        re_wid = wid * (1 - self._args.wheel_ratio) / 2 * self._args.volum_ratio
        re_wid = self._v_tag_radius * 3 if self._v_tag_radius * 3 < re_wid else re_wid

        bar_1_center = ((wid - self._radius * 2) / 4, hig / 2)
        self._bar_1_box = (bar_1_center[0] - re_wid / 2, bar_1_center[1] - hig * self._args.volum_ratio / 2, re_wid, hig * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_1_box[0], self._bar_1_box[1], self._bar_1_box[0], self._bar_1_box[3])
        lgrad.setColorAt(1.0, Qt.white)
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_1_box)

        self._cir_1_center = (bar_1_center[0], self._bar_1_box[1] + self._bar_1_box[3] * bar_v)
        cir_1_box = get_outer_box(self._cir_1_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_1_box)

        bar_2_center = (wid - (wid - self._radius * 2) / 4, hig / 2)
        self._bar_2_box = (bar_2_center[0] - re_wid / 2, bar_2_center[1] - hig * self._args.volum_ratio / 2, re_wid, hig * self._args.volum_ratio)
        painter.setPen(QPen(QColor(*self._args.wheel_ed_color), self._args.wheel_ed_wid))
        lgrad = QLinearGradient(self._bar_2_box[0], self._bar_2_box[1], self._bar_2_box[0], self._bar_2_box[3])
        lgrad.setColorAt(1.0, QColor(*bar_rgb))
        lgrad.setColorAt(0.0, Qt.black)
        painter.setBrush(lgrad)
        painter.drawRect(*self._bar_2_box)

        self._cir_2_center = (bar_2_center[0], self._bar_2_box[1] + self._bar_2_box[3] * bar_v)
        cir_2_box = get_outer_box(self._cir_2_center, self._v_tag_radius)
        painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawEllipse(*cir_2_box)

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = np.array((event.x(), event.y()))
            self._backup = self._args.sys_color_set.backup()

            if np.linalg.norm(point - self._center) < self._radius:
                already_accepted = False

                for idx in range(5):
                    if np.linalg.norm(point - self._tag_center[idx]) < self._tag_radius:
                        self._args.sys_activated_idx = idx

                        self.ps_index_changed.emit(True)
                        already_accepted = True

                        event.accept()
                        # self.update() is completed by 
                        # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                        # same below.
                        break

                if already_accepted or self._args.press_move:
                    self._pressed_in_wheel = True

                    color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                    color.s = np.linalg.norm(point - self._center) / self._radius
                    color.h = get_theta_center(self._center, point)

                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                    self.ps_color_changed.emit(True)

                    event.accept()
                    # self.update() is completed by 
                    # self._wget_cube_table.ps_color_changed.connect(lambda x: self._wget_wheel.update()) in main.py.
                    # same below.

                else:
                    event.ignore()

            elif self._bar_1_box[0] < point[0] < self._bar_1_box[0] + self._bar_1_box[2] and self._bar_1_box[1] < point[1] < self._bar_1_box[1] + self._bar_1_box[3]:
                if np.linalg.norm(point - self._cir_1_center) < self._v_tag_radius or self._args.press_move:
                    self._pressed_in_bar_1 = True

                    v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
                    color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                    color.v = v

                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                    self.ps_color_changed.emit(True)

                    event.accept()

                else:
                    event.ignore()

            elif self._bar_2_box[0] < point[0] < self._bar_2_box[0] + self._bar_2_box[2] and self._bar_2_box[1] < point[1] < self._bar_2_box[1] + self._bar_2_box[3]:
                if np.linalg.norm(point - self._cir_2_center) < self._v_tag_radius or self._args.press_move:
                    self._pressed_in_bar_2 = True

                    v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
                    color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
                    color.v = v

                    self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
                    self.ps_color_changed.emit(True)

                    event.accept()

                else:
                    event.ignore()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        point = np.array((event.x(), event.y()))

        if self._pressed_in_wheel:
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.s = np.linalg.norm(point - self._center) / self._radius
            color.h = get_theta_center(self._center, point)

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_1:
            v = (point[1] - self._bar_1_box[1]) / self._bar_1_box[3]
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.v = v

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        elif self._pressed_in_bar_2:
            v = (point[1] - self._bar_2_box[1]) / self._bar_2_box[3]
            color = Color(self._backup[self._args.sys_activated_idx], tp="color", overflow=self._backup[0].get_overflow())
            color.v = v

            self._args.sys_color_set.recover(self._backup)
            self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)
            self.ps_color_changed.emit(True)

            event.accept()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if self._pressed_in_wheel or self._pressed_in_bar_1 or self._pressed_in_bar_2:
            self._pressed_in_wheel = False
            self._pressed_in_bar_1 = False
            self._pressed_in_bar_2 = False

        event.ignore()
