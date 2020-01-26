# -*- coding: utf-8 -*-

import os
import sys
import time
import numpy as np
from PIL import Image as PImage
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QMessageBox, QFileDialog, QShortcut, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QCursor, QKeySequence
from cguis.resource import view_rc
from clibs.image3c import Image3C
from clibs.transpt import get_outer_box
from clibs.color import Color


class OverLabel(QLabel):
    """
    OverLabel object based on QLabel. Init a over label above Image.
    """

    ps_circle_moved = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init OverLabel label.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._pressed = False

        self.croping = False
        self.locating = False
        self.locations = [None, None, None, None, None]

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        idx_seq = list(range(5))
        idx_seq = idx_seq[self._args.sys_activated_idx + 1: ] + idx_seq[: self._args.sys_activated_idx + 1]

        for idx in idx_seq:
            if self.locations[idx]:
                pt_xy = np.array((self.locations[idx][0] * self.width(), self.locations[idx][1] * self.height()))
                pt_box = get_outer_box(pt_xy, self._args.circle_dist)

                if idx == self._args.sys_activated_idx:
                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                else:
                    painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

                painter.setBrush(QColor(*self._args.sys_color_set[idx].rgb))
                painter.drawEllipse(*pt_box)

        if isinstance(self.croping, tuple):
            painter.setPen(QPen(Qt.NoPen))
            painter.setBrush(QColor(255, 255, 255, 160))

            croping = self.sort_croping()
            croping = (int(self.width() * croping[0]), int(self.height() * croping[1]), int(self.width() * croping[2]), int(self.height() * croping[3]))
            self.draw_rect(painter, 0, 0, croping[0], self.height())
            self.draw_rect(painter, croping[2], 0, self.width(), self.height())
            self.draw_rect(painter, croping[0], 0, croping[2], croping[1])
            self.draw_rect(painter, croping[0], croping[3], croping[2], self.height())

            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
            painter.setBrush(QBrush(Qt.NoBrush))

            if 0 <= self.croping[0] <= self.width():
                painter.drawLine(QPoint(self.croping[0] * self.width(), 0), QPoint(self.croping[0] * self.width(), self.height()))

            if 0 <= self.croping[1] <= self.height():
                painter.drawLine(QPoint(0, self.croping[1] * self.height()), QPoint(self.width(), self.croping[1] * self.height()))

            if 0 <= self.croping[2] <= self.width():
                painter.drawLine(QPoint(self.croping[2] * self.width(), 0), QPoint(self.croping[2] * self.width(), self.height()))

            if 0 <= self.croping[3] <= self.height():
                painter.drawLine(QPoint(0, self.croping[3] * self.height()), QPoint(self.width(), self.croping[3] * self.height()))

        elif isinstance(self.locating, tuple):
            painter.setPen(QPen(Qt.NoPen))
            painter.setBrush(QColor(255, 255, 255, 160))

            painter.drawRect(0, 0, self.width(), self.height())

            painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))
            painter.setBrush(QBrush(Qt.NoBrush))

            if 0 <= self.locating[0] <= self.width():
                painter.drawLine(QPoint(self.locating[0] * self.width(), 0), QPoint(self.locating[0] * self.width(), self.height()))

            if 0 <= self.locating[1] <= self.height():
                painter.drawLine(QPoint(0, self.locating[1] * self.height()), QPoint(self.width(), self.locating[1] * self.height()))

        elif self.croping or self.locating:
            painter.setPen(QPen(Qt.NoPen))
            painter.setBrush(QColor(255, 255, 255, 160))

            painter.drawRect(0, 0, self.width(), self.height())

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mousePressEvent(self, event):
        if self.croping or self.locating:
            event.ignore()
            return

        point = np.array((event.x(), event.y()))
        already_accepted = False

        for idx in range(5):
            if self.locations[idx] and np.linalg.norm(point - np.array(self.locations[idx]) * np.array((self.width(), self.height()))) < self._args.circle_dist:
                self._args.sys_activated_idx = idx
                already_accepted = True

                break

        if event.button() == Qt.LeftButton and (self._args.press_move or already_accepted or (not self.locations[self._args.sys_activated_idx])):
            loc = [point[0] / self.width(), point[1] / self.height()]
            loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
            loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
            loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
            loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

            self.locations[self._args.sys_activated_idx] = tuple(loc)
            self.ps_circle_moved.emit(True)

            self._pressed = True

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self.croping:
            event.ignore()
            return

        if self._pressed:
            point = np.array((event.x(), event.y()))

            loc = [point[0] / self.width(), point[1] / self.height()]
            loc[0] = 0.0 if loc[0] < 0.0 else loc[0]
            loc[0] = 1.0 if loc[0] > 1.0 else loc[0]
            loc[1] = 0.0 if loc[1] < 0.0 else loc[1]
            loc[1] = 1.0 if loc[1] > 1.0 else loc[1]

            self.locations[self._args.sys_activated_idx] = tuple(loc)
            self.ps_circle_moved.emit(True)

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._pressed = False

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def draw_rect(self, painter, x0, y0, x1, y1):
        """
        Draw rect by two points.
        """

        if x0 == x1 or y0 == y1:
            return

        painter.drawRect(x0, y0, x1 - x0, y1 - y0)

    def sort_croping(self):
        """
        Sort the croping value from mouse move to standard value.
        """

        croping = list(self.croping)
        croping[0] = 0.0 if croping[0] < 0.0 else croping[0]
        croping[1] = 0.0 if croping[1] < 0.0 else croping[1]
        croping[2] = 0.0 if croping[2] < 0.0 else croping[2]
        croping[3] = 0.0 if croping[3] < 0.0 else croping[3]
        croping[0] = 1.0 if croping[0] > 1.0 else croping[0]
        croping[1] = 1.0 if croping[1] > 1.0 else croping[1]
        croping[2] = 1.0 if croping[2] > 1.0 else croping[2]
        croping[3] = 1.0 if croping[3] > 1.0 else croping[3]

        if croping[0] > croping[2]:
            croping[0], croping[2] = croping[2], croping[0]

        if croping[1] > croping[3]:
            croping[1], croping[3] = croping[3], croping[1]

        return croping

    def revise_croping(self, rgb_data_shape):
        """
        Revise the croping value from mouse move to standard value (full in image).
        """

        croping = self.sort_croping()

        min_wid_rto = 5.0 / rgb_data_shape[1]
        min_hig_rto = 5.0 / rgb_data_shape[0]

        if croping[2] - croping[0] < min_wid_rto:
            croping[2] = croping[0] + min_wid_rto

            if croping[2] > 1.0:
                croping[2] = 1.0
                croping[0] = 1.0 - min_wid_rto

        if croping[3] - croping[1] < min_hig_rto:
            croping[3] = croping[1] + min_hig_rto

            if croping[3] > 1.0:
                croping[3] = 1.0
                croping[1] = 1.0 - min_hig_rto

        self.croping = tuple(croping)

    def revise_locating(self):
        """
        Revise the locating value from mouse move to standard value (full in image).
        """

        locating = list(self.locating)

        locating[0] = 0.0 if locating[0] < 0.0 else locating[0]
        locating[1] = 0.0 if locating[1] < 0.0 else locating[1]
        locating[0] = 1.0 if locating[0] > 1.0 else locating[0]
        locating[1] = 1.0 if locating[1] > 1.0 else locating[1]

        self.locating = tuple(locating)


class Image(QWidget):
    """
    Image object based on QWidget. Init a image pannel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)
    ps_image_changed = pyqtSignal(bool)
    ps_status_changed = pyqtSignal(tuple)
    ps_recover_channel = pyqtSignal(bool)
    ps_modify_rule = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init Image pannel.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._categories = set()
        self._drop_image = None
        self._move_pos = None
        self._start_pt = None
        self._is_croping = False
        self._is_locating = False
        self._enhance_lock = False
        self._resizing_image = False

        # load translations.
        self._func_tr_()

        # init qt args.
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAcceptDrops(True)

        self._tip_label = QLabel(self)
        self._tip_label.setWordWrap(True)

        self._loading_bar = QProgressBar(self)
        self._loading_bar.setMaximum(100)
        self._loading_bar.setValue(0)

        self._ico = QImage(":/images/images/icon_grey_1024.png")
        self._ico_label = QLabel(self)

        self._image3c = Image3C(self._args.global_temp_dir)
        self._image3c.ps_describe.connect(self.update_loading_label)
        self._image3c.ps_proceses.connect(self.update_loading_bar)
        self._image3c.ps_finished.connect(self.loading_finished)
        self._image3c.ps_enhanced.connect(self.enhance_finished)
        self._image3c.ps_extracts.connect(self.extract_finished)

        self.overlabel_display = OverLabel(self, self._args)
        self.overlabel_display.ps_circle_moved.connect(lambda x: self.modify_color_loc())

        shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        shortcut.activated.connect(self.clipboard_in)

    def paintEvent(self, event):
        if not self._image3c.img_data:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.show()
            self.overlabel_display.hide()

            painter = QPainter()
            painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            painter.setPen(QPen(Qt.black, Qt.PenStyle(Qt.DashLine), 3))
            painter.setBrush(Qt.white)
            self._tip_box = (self.width() * 0.2, self.height() * 0.2, self.width() * 0.6, self.height() * 0.6)
            radius = min(self.width() * 0.1, self.height() * 0.1)
            painter.drawRoundedRect(*self._tip_box, radius, radius)

            painter.end()

            self._tip_label.setGeometry(QRect(*self._tip_box))

            self._tip_label.setText(self._action_descs[0])
            self._tip_label.setAlignment(Qt.AlignCenter)

        elif self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self._loading_bar.show()
            self._ico_label.show()
            self._tip_label.show()
            self.overlabel_display.hide()

            bar_wid = self.width() * 0.8
            bar_hig = self.height() * 0.1

            self._loading_bar.setGeometry((self.width() - bar_wid) / 2, self.height() - bar_hig * 1.2, bar_wid, bar_hig)

            resized_img = self._ico.scaled(self.width() * 0.8, self.height() * 0.8, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()

            self._ico_label.setPixmap(QPixmap.fromImage(resized_img))
            self._ico_label.setGeometry((self.width() - img_wid) / 2, bar_hig * 0.2, img_wid, img_hig)

            self._tip_label.setGeometry((self.width() - bar_wid) / 2, self.height() - bar_hig * 2.2, bar_wid, bar_hig)

        else:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.hide()
            self.overlabel_display.show()

            if not self._image3c.display:
                self._image3c.load_image(self._args.sys_category, self._args.sys_channel)
                self._resizing_image = True

            if self._image3c.display:
                if not self._move_pos:
                    self.home()

                self._move_pos[0] = self.width() - 2 if self._move_pos[0] > self.width() - 2 else self._move_pos[0]
                self._move_pos[0] = 2 - self._move_pos[2] if self._move_pos[0] < 2 - self._move_pos[2] else self._move_pos[0]
                self._move_pos[1] = self.height() - 2 if self._move_pos[1] > self.height() - 2 else self._move_pos[1]
                self._move_pos[1] = 2 - self._move_pos[3] if self._move_pos[1] < 2 - self._move_pos[3] else self._move_pos[1]

                # aspect ratio mode: IgnoreAspectRatio, KeepAspectRatio and KeepAspectRatioByExpanding.
                if self._resizing_image:
                    resized_img = self._image3c.display.scaled(self._move_pos[2], self._move_pos[3], Qt.IgnoreAspectRatio)
                    self.overlabel_display.setPixmap(QPixmap.fromImage(resized_img))
                    self._resizing_image = False

                self.overlabel_display.setGeometry(*self._move_pos)

                if isinstance(self.overlabel_display.croping, tuple):
                    painter = QPainter()
                    painter.begin(self)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.setRenderHint(QPainter.TextAntialiasing, True)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                    painter.drawLine(QPoint(self.overlabel_display.croping[0] * self.overlabel_display.width() + self.overlabel_display.x(), 0), QPoint(self.overlabel_display.croping[0] * self.overlabel_display.width() + self.overlabel_display.x(), self.height()))
                    painter.drawLine(QPoint(0, self.overlabel_display.croping[1] * self.overlabel_display.height() + self.overlabel_display.y()), QPoint(self.width(), self.overlabel_display.croping[1] * self.overlabel_display.height() + self.overlabel_display.y()))

                    painter.drawLine(QPoint(self.overlabel_display.croping[2] * self.overlabel_display.width() + self.overlabel_display.x(), 0), QPoint(self.overlabel_display.croping[2] * self.overlabel_display.width() + self.overlabel_display.x(), self.height()))
                    painter.drawLine(QPoint(0, self.overlabel_display.croping[3] * self.overlabel_display.height() + self.overlabel_display.y()), QPoint(self.width(), self.overlabel_display.croping[3] * self.overlabel_display.height() + self.overlabel_display.y()))

                    painter.end()

                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format(self.overlabel_display.croping[2] * 100), "{:.1f}".format(self.overlabel_display.croping[3] * 100)))

                elif isinstance(self.overlabel_display.locating, tuple):
                    painter = QPainter()
                    painter.begin(self)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.setRenderHint(QPainter.TextAntialiasing, True)
                    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                    painter.drawLine(QPoint(self.overlabel_display.locating[0] * self.overlabel_display.width() + self.overlabel_display.x(), 0), QPoint(self.overlabel_display.locating[0] * self.overlabel_display.width() + self.overlabel_display.x(), self.height()))
                    painter.drawLine(QPoint(0, self.overlabel_display.locating[1] * self.overlabel_display.height() + self.overlabel_display.y()), QPoint(self.width(), self.overlabel_display.locating[1] * self.overlabel_display.height() + self.overlabel_display.y()))

                    painter.end()

                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format(self.overlabel_display.locating[0] * 100), "{:.1f}".format(self.overlabel_display.locating[1] * 100)))

                elif self.overlabel_display.locations[self._args.sys_activated_idx]:
                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0], "{:.1f}".format(self.overlabel_display.locations[self._args.sys_activated_idx][0] * 100), "{:.1f}".format(self.overlabel_display.locations[self._args.sys_activated_idx][1] * 100)))

                else:
                    self.ps_status_changed.emit((self._image3c.rgb_data.shape[1], self._image3c.rgb_data.shape[0]))

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mouseDoubleClickEvent(self, event):
        if not self._image3c.img_data and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._tip_box[0] < p_x < (self._tip_box[0] + self._tip_box[2]) and self._tip_box[1] < p_y < (self._tip_box[1] + self._tip_box[3]):
                self.open_image_dialog()

                event.accept()
                self.update()

            else:
                event.ignore()

    def dragEnterEvent(self, event):
        try:
            image = event.mimeData().urls()[0].toLocalFile()

        except Exception as err:
            event.ignore()
            return

        if image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff"):
            self._drop_image = image
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if self._drop_image:
            self.open_image(self._drop_image)
            self._drop_image = None

            event.accept()

        else:
            event.ignore()

    def wheelEvent(self, event):
        if self.overlabel_display.isVisible() and self._image3c.display:
            point = (event.x(), event.y())
            ratio = (event.angleDelta() / 120).y()

            if ratio:
                ratio = ratio * self._args.zoom_step if ratio > 0 else -1 * ratio / self._args.zoom_step

            else:
                ratio = 1

            self.zoom(ratio, point)

            event.accept()
            # self.update() is completed by self.zoom.
            # self.update()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        if self.overlabel_display.isVisible() and self._image3c.display:
            if event.button() == Qt.MidButton:
                self.setCursor(QCursor(Qt.ClosedHandCursor))
                self._start_pt = (event.x(), event.y())

                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self.overlabel_display.croping:
                self._is_croping = True
                self.overlabel_display.croping = (
                    (event.x() - self.overlabel_display.x()) / self.overlabel_display.width(),
                    (event.y() - self.overlabel_display.y()) / self.overlabel_display.height(),
                    (event.x() - self.overlabel_display.x()) / self.overlabel_display.width(),
                    (event.y() - self.overlabel_display.y()) / self.overlabel_display.height(),
                )

                event.accept()
                self.update()

            elif event.button() == Qt.LeftButton and self.overlabel_display.locating:
                self._is_locating = True
                self.overlabel_display.locating = (
                    (event.x() - self.overlabel_display.x()) / self.overlabel_display.width(),
                    (event.y() - self.overlabel_display.y()) / self.overlabel_display.height(),
                )

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton and self.overlabel_display.croping:
                self._is_croping = False
                self.overlabel_display.croping = False

                event.accept()
                self.update()

            elif event.button() == Qt.RightButton and self.overlabel_display.locating:
                self._is_locating = False
                self.overlabel_display.locating = False

                event.accept()
                self.update()

            else:
                event.ignore()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._start_pt:
            point = (event.x(), event.y())

            if self._args.rev_direct:
                self.move(self._start_pt[0] - point[0], self._start_pt[1] - point[1])

            else:
                self.move(point[0] - self._start_pt[0], point[1] - self._start_pt[1])

            self._start_pt = point

            event.accept()
            # self.update() is completed by self.move.
            # self.update()

        elif self._is_croping:
            self.overlabel_display.croping = (
                self.overlabel_display.croping[0],
                self.overlabel_display.croping[1],
                (event.x() - self.overlabel_display.x()) / self.overlabel_display.width(),
                (event.y() - self.overlabel_display.y()) / self.overlabel_display.height(),
            )

            event.accept()
            self.update()

        elif self._is_locating:
            self.overlabel_display.locating = (
                (event.x() - self.overlabel_display.x()) / self.overlabel_display.width(),
                (event.y() - self.overlabel_display.y()) / self.overlabel_display.height(),
            )

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self._start_pt = None

        if self._is_croping:
            self.overlabel_display.revise_croping(self._image3c.rgb_data.shape)
            self._is_croping = False

            self.update()

        if self._is_locating:
            self.overlabel_display.revise_locating()
            self._is_locating = False

            self.update()

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def zoom(self, ratio, center):
        """
        Zoom displayed image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if center == "default":
            center = (self.width() / 2, self.height() / 2)

        x = self.overlabel_display.x()
        y = self.overlabel_display.y()
        wid = self.overlabel_display.width()
        hig = self.overlabel_display.height()

        x = (x - center[0]) * ratio + center[0]
        y = (y - center[1]) * ratio + center[1]

        self._move_pos = [int(round(x)), int(round(y)), int(round(wid * ratio)), int(round(hig * ratio))]
        self._resizing_image = True

        self.update()

    def move(self, shift_x, shift_y):
        """
        Move displayed image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        x = self.overlabel_display.x()
        y = self.overlabel_display.y()
        wid = self.overlabel_display.width()
        hig = self.overlabel_display.height()

        if self._args.rev_direct:
            x = x - shift_x
            y = y - shift_y

        else:
            x = x + shift_x
            y = y + shift_y

        self._move_pos = [x, y, wid, hig]
        self._resizing_image = False

        self.update()

    def home(self):
        """
        Home displayed image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        img_wid = self._image3c.display.size().width()
        img_hig = self._image3c.display.size().height()

        ratio = min(self.width() / img_wid, self.height() / img_hig)
        self._move_pos = [
            int(round((self.width() - img_wid * ratio) / 2)),
            int(round((self.height() - img_hig * ratio) / 2)),
            int(round(img_wid * ratio)),
            int(round(img_hig * ratio)),
        ]
        self._resizing_image = True

        self.update()

    def open_image_dialog(self):
        """
        Open a image dialog.
        """

        if not self.isVisible():
            return

        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff)".format(*self._extend_descs)
        cb_file = QFileDialog.getOpenFileName(None, self._action_descs[1], self._args.usr_image, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
            self.open_image(cb_file[0])

        else:
            # closed without open a file.
            return

    def open_image(self, image, script=""):
        """
        Open a image.
        """

        if isinstance(script, tuple) and (not self.isVisible()):
            return

        if script and (not self._image3c.img_data):
            return

        if self._image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if not self._args.check_temp_dir():
            self.warning(self._image_errs[2])
            return

        if not isinstance(script, tuple):
            try:
                img_data = PImage.open(image)

            except Exception as err:
                self.warning(self._image_errs[4])
                return

            self._image3c.img_data = img_data

        self._categories = set()

        self._args.sys_category = 0
        self._args.sys_channel = 0
        self.ps_image_changed.emit(True)

        self.overlabel_display.locations = [None, None, None, None, None]
        self._image3c.display = None

        self._image3c.ori_display_data = None
        self._image3c.res_display_data = None
        self._image3c.rev_display_data = None

        self._image3c.rgb_data = None
        self._image3c.hsv_data = None

        if isinstance(script, tuple):
            if script[0] in ("ZOOM", "CROP"):
                self._move_pos = None

            self._image3c.run_args = script
            self._image3c.run_category = "init"
            self._image3c.start()

        else:
            self._move_pos = None

            self._image3c.run_args = None

            self._image3c.run_category = "init"
            self._image3c.start()

        self.update()

    def open_category(self):
        """
        Open this image in other category.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible()):
            return

        if not self._image3c.img_data:
            return

        if not self._args.check_temp_dir():
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[2])
            return

        if self._enhance_lock:
            self.ps_recover_channel.emit(True)
            self.warning(self._image_errs[1])
            return

        self._image3c.display = None

        self._image3c.ori_display_data = None
        self._image3c.res_display_data = None
        self._image3c.rev_display_data = None

        if self._args.sys_category * 10 + self._args.sys_channel not in self._categories:
            self._image3c.run_category = self._args.sys_category
            self._image3c.start()

        self.update()

    def extract_image(self, values):
        """
        Modify r, g or (and) b values to enhance or inverse the contrast of image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        self._image3c.run_args = (self._args.rand_num, values)
        self._image3c.run_category = "extract"
        self._image3c.start()

        self.update()

    def enhance_image(self, values):
        """
        Modify r, g or (and) b values to enhance or inverse the contrast of image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if values[0][:5] == "cover":
            cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff)".format(*self._extend_descs)
            cb_file = QFileDialog.getOpenFileName(None, self._action_descs[3], self._args.usr_image, filter=cb_filter)

            if cb_file[0]:
                self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
                values = list(values) + [os.path.abspath(cb_file[0])]

            else:
                # closed without open a file.
                return

        self._enhance_lock = True

        self._image3c.run_args = values[1:]
        self._image3c.run_category = values[0]
        self._image3c.start()

        self.update()

    def crop_image(self, value):
        """
        Crop image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if self.overlabel_display.locating:
            return

        if self._image3c.isRunning() or self._enhance_lock:
            self.warning(self._image_errs[1])
            return

        if value:
            if isinstance(self.overlabel_display.croping, tuple):
                self.open_image("", ("CROP", self.overlabel_display.croping))

            else:
                self.overlabel_display.croping = True

        else:
            self.overlabel_display.croping = False

        self.update()

    def replace_color(self, value):
        """
        Replace color.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        if self.overlabel_display.croping:
            return

        if value[0]:
            if isinstance(self.overlabel_display.locating, tuple):
                shape = self._image3c.rgb_data.shape

                rgb = self._image3c.rgb_data[int(self.overlabel_display.locating[1] * (shape[0] - 1))][int(self.overlabel_display.locating[0] * (shape[1] - 1))]
                separ = []
                fact = []

                if value[0] == 1:
                    for i in range(3):
                        if self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] > rgb[i]:
                            separ.append(rgb[i] - rgb[i] * value[3])
                            fact.append((self._args.sys_color_set[self._args.sys_activated_idx].rgb[i] - rgb[i]) / (255 - rgb[i]))

                        else:
                            separ.append(rgb[i] + 0.00001 + (255.0 - rgb[i]) * value[3])
                            fact.append((rgb[i] - self._args.sys_color_set[self._args.sys_activated_idx].rgb[i]) / rgb[i])

                    self._image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2])
                    self._image3c.run_category = "enhance_rgb"

                elif value[0] == 2:
                    hsv = Color.rgb2hsv(rgb)
                    separ.append((hsv[0] + 360.0 * value[3]) % 360.0)
                    fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[0] - hsv[0]) / 360)

                    if self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] > hsv[1]:
                        separ.append(hsv[1] - hsv[1] * value[3])
                        fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[1] - hsv[1]) / (1.0 - hsv[1]))

                    else:
                        separ.append(hsv[1] + 0.00001 + (1.0 - hsv[1]) * value[3])
                        fact.append((hsv[1] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[1]) / hsv[1])

                    if self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] > hsv[2]:
                        separ.append(hsv[2] - hsv[2] * value[3])
                        fact.append((self._args.sys_color_set[self._args.sys_activated_idx].hsv[2] - hsv[2]) / (1.0 - hsv[2]))

                    else:
                        separ.append(hsv[2] + 0.00001 + (1.0 - hsv[1]) * value[3])
                        fact.append((hsv[2] - self._args.sys_color_set[self._args.sys_activated_idx].hsv[2]) / hsv[2])

                    self._image3c.run_args = ((0, 1, 2), tuple(separ), tuple(fact), value[1], value[2])
                    self._image3c.run_category = "enhance_hsv"

                self._image3c.start()

                self._enhance_lock = True

            else:
                self.overlabel_display.locating = True

        else:
            self.overlabel_display.locating = False

        self.update()

    def update_loading_label(self, idx):
        """
        Loading descriptions when importing a image.
        """

        self._tip_label.setText(self._image_descs[idx])
        self._tip_label.setAlignment(Qt.AlignCenter)

        self.update()

    def update_loading_bar(self, idx):
        """
        Loading process when importing a image.
        """

        self._loading_bar.setValue(idx)

        self.update()

    def loading_finished(self, idx):
        """
        Loading finished.
        """

        self._categories.add(idx)
        self.overlabel_display.croping = False
        self.overlabel_display.locating = False
        self._resizing_image = True

        self.update()

    def extract_finished(self, value):
        """
        Enhance finished.
        """

        self._args.hm_rule = "custom"
        self.ps_modify_rule.emit(True)

        self.overlabel_display.locations = value

        for i in range(5):
            rgb = self._image3c.rgb_data[int(value[i][1] * (self._image3c.rgb_data.shape[0] - 1))][int(value[i][0] * (self._image3c.rgb_data.shape[1] - 1))]

            color = Color(rgb, tp="rgb", overflow=self._args.sys_color_set.get_overflow())
            self._args.sys_color_set.modify(self._args.hm_rule, i, color)

        self.ps_color_changed.emit(True)
        # similar to modify_color_loc,
        # update_color_loc() is completed by 
        # self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color()) in main.py.

        self.update()

    def enhance_finished(self, idx):
        """
        Enhance finished.
        """

        if idx == 2:
            self.warning(self._image_errs[6])

        if idx == 3:
            self.warning(self._image_errs[7])

        self._enhance_lock = False
        self._resizing_image = True
        self.overlabel_display.locating = False

        self.update()

    def modify_color_loc(self):
        """
        Modify color set by overlabel. 
        """

        if self.overlabel_display.locations[self._args.sys_activated_idx]:
            shape = self._image3c.rgb_data.shape

            loc = self.overlabel_display.locations[self._args.sys_activated_idx]
            rgb = self._image3c.rgb_data[int(loc[1] * (shape[0] - 1))][int(loc[0] * (shape[1] - 1))]

            if not (rgb == self._args.sys_color_set[self._args.sys_activated_idx].rgb).all():
                color = Color(rgb, tp="rgb", overflow=self._args.sys_color_set.get_overflow())
                self._args.sys_color_set.modify(self._args.hm_rule, self._args.sys_activated_idx, color)

        self.ps_color_changed.emit(True)
        # update_color_loc() is completed by 
        # self._wget_image.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color()) in main.py.

    def update_color_loc(self):
        """
        Update color set by overlabel. 
        """

        for idx in range(5):
            if self.overlabel_display.locations[idx]:
                shape = self._image3c.rgb_data.shape

                loc = self.overlabel_display.locations[idx]
                rgb = self._image3c.rgb_data[int(loc[1] * (shape[0] - 1))][int(loc[0] * (shape[1] - 1))]

                if not (rgb == self._args.sys_color_set[idx].rgb).all():
                    self.overlabel_display.locations[idx] = None

        self.overlabel_display.update()

    def freeze_image(self, value):
        """
        Freeze current image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        if self._image3c.isRunning():
            self.warning(self._image_errs[1])
            return

        load_image = self._image3c.save_load_data(self._image3c.display)

        if load_image:
            self.open_image(load_image)

        else:
            self.warning(self._image_errs[5])

    def print_image(self, value):
        """
        Exec print image.
        """

        if not (self.isVisible() and self.overlabel_display.isVisible() and self._image3c.display):
            return

        name = "{}".format(time.strftime("DigiPale_Image_%Y_%m_%d.png", time.localtime()))

        cb_filter = "{} (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; {} (*.png);; {} (*.bmp);; {} (*.jpg *.jpeg);; {} (*.tif *.tiff)".format(*self._extend_descs)
        cb_file = QFileDialog.getSaveFileName(None, self._action_descs[2], os.sep.join((self._args.usr_image, name)), filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))

        else:
            # closed without open a file.
            return

        self._image3c.display.save(cb_file[0])

    def clipboard_in(self):
        """
        Load image from clipboard.
        """

        clipboard = QApplication.clipboard().mimeData()

        if clipboard.hasUrls():
            try:
                image = clipboard.urls()[0].toLocalFile()

            except Exception as err:
                return

            if image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff") and os.path.isfile(image):
                self.open_image(image)

        elif clipboard.hasImage():
            load_image = self._image3c.save_load_data(clipboard.imageData())

            if load_image:
                self.open_image(load_image)

    def update_all(self):
        self.overlabel_display.update()
        self.update()

    def warning(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(self._image_errs[0])
        box.setText(text)
        box.setIcon(QMessageBox.Warning)
        box.addButton(self._image_errs[3], QMessageBox.AcceptRole)

        box.exec_()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._action_descs = (
            _translate("Image", "Double click here to open an image."),
            _translate("Image", "Open"),
            _translate("Image", "Print"),
            _translate("Image", "Cover"),
        )

        self._image_errs = (
            _translate("Image", "Error"),
            _translate("Image", "Could not process image. There is a process of image not finished."),
            _translate("Image", "Could not create temporary dir. Dir is not created."),
            _translate("Image", "OK"),
            _translate("Image", "Could not open image. This image is broken."),
            _translate("Image", "Could not process image. Translation is not completed."),
            _translate("Image", "Could not process image. The size of image is not suitable."),
            _translate("Image", "Could not process image. This image is invalid."),
        )

        self._image_descs = (
            _translate("Image", "Finishing."),
            _translate("Image", "Loading RGB data."),
            _translate("Image", "Saving RGB data."),
            _translate("Image", "Loading HSV data."),
            _translate("Image", "Saving HSV data."),
            _translate("Image", "Loading RGB vertical edge data."),
            _translate("Image", "Saving RGB vertical edge data."),
            _translate("Image", "Loading RGB horizontal edge data."),
            _translate("Image", "Saving RGB horizontal edge data."),
            _translate("Image", "Loading RGB final edge data."),
            _translate("Image", "Saving RGB final edge data."),
            _translate("Image", "Loading HSV vertical edge data."),
            _translate("Image", "Saving HSV vertical edge data."),
            _translate("Image", "Loading HSV horizontal edge data."),
            _translate("Image", "Saving HSV horizontal edge data."),
            _translate("Image", "Loading HSV final edge data."),
            _translate("Image", "Saving HSV final edge data."),
            _translate("Image", "Applying filter to image data."),
        )

        self._extend_descs = (
            _translate("Image", "All Images"),
            _translate("Image", "PNG Image"),
            _translate("Image", "BMP Image"),
            _translate("Image", "JPG Image"),
            _translate("Image", "TIF Image"),
        )
