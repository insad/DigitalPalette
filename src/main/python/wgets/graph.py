# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QCoreApplication, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QImage
from cguis.resource import view_rc
from clibs.image3c import Image3C
from clibs.transpt import get_outer_box
from clibs.color import Color


class OverLabel(QLabel):
    """
    OverLabel object based on QLabel. Init a over label above graph.
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
        self.locations = [None, None, None, None, None]

    def paintEvent(self, event):
        super().paintEvent(event)

        self._wid = self.geometry().width()
        self._hig = self.geometry().height()

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        for idx in range(5):
            if self.locations[idx]:
                pt_xy = np.array((self.locations[idx][0] * self._wid, self.locations[idx][1] * self._hig))
                pt_box = get_outer_box(pt_xy, self._args.circle_dist)

                if idx == self._args.sys_activated_idx:
                    painter.setPen(QPen(QColor(*self._args.positive_color), self._args.positive_wid))

                else:
                    painter.setPen(QPen(QColor(*self._args.negative_color), self._args.negative_wid))

                painter.setBrush(QColor(*self._args.sys_color_set[idx].rgb))
                painter.drawEllipse(*pt_box)

        painter.end()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and not self._image_imported:
            p_x = event.x()
            p_y = event.y()

            box = (self._wid * 0.2, self._hig * 0.2, self._wid * 0.6, self._hig * 0.6)

            if box[0] < p_x < (box[0] + box[2]) and box[1] < p_y < (box[1] + box[3]):
                self.slot_open_graph()

                event.accept()
                self.update()
            else:
                event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = np.array((event.x(), event.y()))

            loc = [point[0] / self._wid, point[1] / self._hig]
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
        if self._pressed:
            point = np.array((event.x(), event.y()))

            loc = [point[0] / self._wid, point[1] / self._hig]
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


class Graph(QWidget):
    """
    Graph object based on QWidget. Init a graph pannel in workarea.
    """

    ps_color_changed = pyqtSignal(bool)

    def __init__(self, wget, args):
        """
        Init Graph pannel.
        """

        super().__init__(wget)

        # load args.
        self._args = args
        self._categories = []
        self._drag_image = None
        self._move_pos = None
        self._start_pt = None

        # load translations.
        self._func_tr_()

        # qt args.
        self.setAcceptDrops(True)

        self._tip_label = QLabel(self)
        self._tip_label.setWordWrap(True)

        self._loading_bar = QProgressBar(self)
        self._loading_bar.setMaximum(100)
        self._loading_bar.setValue(0)

        self._ico = QImage(":/images/images/icon_grey.png")
        self._ico_label = QLabel(self)

        self._image3c = Image3C()
        self._image3c.ps_describe.connect(self.update_loading_label)
        self._image3c.ps_proceses.connect(self.update_loading_bar)
        self._image3c.ps_finished.connect(self.loading_finished)

        self._display = None
        self.overlabel_display = OverLabel(self, self._args)
        self.overlabel_display.ps_circle_moved.connect(lambda x: self.modify_color_loc())

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()

        if not self._categories:
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
            self._tip_box = (wid * 0.2, hig * 0.2, wid * 0.6, hig * 0.6)
            radius = min(wid * 0.1, hig * 0.1)
            painter.drawRoundedRect(*self._tip_box, radius, radius)

            painter.end()

            self._tip_label.setGeometry(QRect(*self._tip_box))

            self._tip_label.setText(self._graph_descs[0])
            self._tip_label.setAlignment(Qt.AlignCenter)

        elif self._args.sys_category not in self._categories:
            self._loading_bar.show()
            self._ico_label.show()
            self._tip_label.show()
            self.overlabel_display.hide()

            bar_wid = wid * 0.8
            bar_hig = hig * 0.1

            self._loading_bar.setGeometry((wid - bar_wid) / 2, hig - bar_hig * 1.2, bar_wid, bar_hig)

            resized_img = self._ico.scaled(wid * 0.8, hig * 0.8, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()

            self._ico_label.setPixmap(QPixmap.fromImage(resized_img))
            self._ico_label.setGeometry((wid - img_wid) / 2, bar_hig * 0.2, img_wid, img_hig)

            self._tip_label.setGeometry((wid - bar_wid) / 2, hig - bar_hig * 2.2, bar_wid, bar_hig)

        else:
            self._loading_bar.hide()
            self._ico_label.hide()
            self._tip_label.hide()
            self.overlabel_display.show()

            if self._display:
                if not self._move_pos:
                    self.home()

                self._move_pos[0] = wid - 2 if self._move_pos[0] > wid - 2 else self._move_pos[0]
                self._move_pos[0] = 2 - self._move_pos[2] if self._move_pos[0] < 2 - self._move_pos[2] else self._move_pos[0]
                self._move_pos[1] = hig - 2 if self._move_pos[1] > hig - 2 else self._move_pos[1]
                self._move_pos[1] = 2 - self._move_pos[3] if self._move_pos[1] < 2 - self._move_pos[3] else self._move_pos[1]

                resized_img = self._display.scaled(self._move_pos[2], self._move_pos[3], Qt.KeepAspectRatio)

                self.overlabel_display.setPixmap(QPixmap.fromImage(resized_img))
                self.overlabel_display.setGeometry(*self._move_pos)

            else:
                self._display = self._image3c.load_image(self._args.sys_category, self._args.sys_channel)
                
                self.update()

    # ---------- ---------- ---------- Mouse Event Funcs ---------- ---------- ---------- #

    def mouseDoubleClickEvent(self, event):
        if not self._categories and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._tip_box[0] < p_x < (self._tip_box[0] + self._tip_box[2]) and self._tip_box[1] < p_y < (self._tip_box[1] + self._tip_box[3]):
                self.open_image_dialog()

                event.accept()
                self.update()

            else:
                event.ignore()

    def dragEnterEvent(self, event):
        image = event.mimeData().text()

        # ubuntu would add \r\n at end.
        image = image[:-1] if image[-1:] == "\n" else image
        image = image[:-1] if image[-1:] == "\r" else image

        if image[:4] == "file" and image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff"):
            # ubuntu need / at start.
            if sys.platform[:3].lower() == "win":
                self._drag_image = image[8:]

            else:
                self._drag_image = image[7:]

            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if self._drag_image:
            self.open_image(self._drag_image)
            self._drag_image = None

            event.accept()

        else:
            event.ignore()

    def wheelEvent(self, event):
        if not self.overlabel_display.isVisible():
            event.ignore()

        point = (event.x(), event.y())
        ratio = (event.angleDelta() / 120).y()

        if ratio:
            ratio = ratio * self._args.zoom_step if ratio > 0 else -1 * ratio / self._args.zoom_step

        else:
            ratio = 1

        self.zoom(ratio, point)

        event.accept()
        self.update()

    def mousePressEvent(self, event):
        if not self.overlabel_display.isVisible():
            event.ignore()

        if event.button() == Qt.MidButton:
            self._start_pt = (event.x(), event.y())

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._start_pt:
            point = (event.x(), event.y())

            self.move(point[0] - self._start_pt[0], point[1] - self._start_pt[1])
            self._start_pt = point

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._start_pt = None

        event.ignore()

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def zoom(self, ratio, center):
        """
        Zoom displayed image.
        """

        if not self.overlabel_display.isVisible():
            return

        if center == "default":
            center = (self.geometry().width() / 2, self.geometry().height() / 2)

        x = self.overlabel_display.geometry().x()
        y = self.overlabel_display.geometry().y()
        wid = self.overlabel_display.geometry().width()
        hig = self.overlabel_display.geometry().height()

        x = (x - center[0]) * ratio + center[0]
        y = (y - center[1]) * ratio + center[1]

        self._move_pos = [x, y, wid * ratio, hig * ratio]

    def move(self, shift_x, shift_y):
        """
        Move displayed image.
        """

        if not self.overlabel_display.isVisible():
            return

        x = self.overlabel_display.geometry().x()
        y = self.overlabel_display.geometry().y()
        wid = self.overlabel_display.geometry().width()
        hig = self.overlabel_display.geometry().height()

        x = x + shift_x
        y = y + shift_y

        self._move_pos = [x, y, wid, hig]

    def home(self):
        """
        Home displayed image.
        """

        if not self.overlabel_display.isVisible():
            return

        wid = self.geometry().width()
        hig = self.geometry().height()

        img_wid = self._display.size().width()
        img_hig = self._display.size().height()

        ratio = min(wid / img_wid, hig / img_hig)
        self._move_pos = [(wid - img_wid * ratio) / 2, (hig - img_hig * ratio) / 2, img_wid * ratio, img_hig * ratio]

    def open_image_dialog(self):
        """
        Open a image dialog.
        """

        cb_filter = "All Images (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; PNG Image (*.png);; BMP Image (*.bmp);; JPEG Image (*.jpg *.jpeg);; TIFF Image (*.tif *.tiff)"
        cb_file = QFileDialog.getOpenFileName(None, self._graph_descs[1], self._args.usr_image, filter=cb_filter)

        if cb_file[0]:
            self._args.usr_image = os.path.dirname(os.path.abspath(cb_file[0]))
            self.open_image(cb_file[0])

        else:
            # closed without open a file.
            return

    def open_image(self, image):
        """
        Open a image.
        """

        if self._image3c.isRunning():
            QMessageBox.warning(self, self._graph_errs[0], self._graph_errs[1])
            return

        self._categories = []
        self._image3c.initialize(image)
        self.overlabel_display.locations = [None, None, None, None, None]
        self._zoom_rto = None
        self._move_pos = None

        self.open_category()

    def open_category(self):
        """
        Open this image in other category.
        """

        if not self._image3c.run_image:
            return

        if not self._image3c.check_temp_dir():
            QMessageBox.warning(self, self._graph_errs[0], self._graph_errs[2])
            return

        self._display = None

        if self._args.sys_category not in self._categories:
            self._image3c.run_category = self._args.sys_category
            self._image3c.start()

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

        self._categories.append(idx)

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
        # self._wget_graph.ps_color_changed.connect(lambda x: self._wget_cube_table.update_color()) in main.py.

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

    def update_all(self):
        self.overlabel_display.update()
        self.update()

    def closeEvent(self, event):
        """
        Actions before close Graph.
        """

        self._image3c.remove_temp_dir()

    # ---------- ---------- ---------- Translations ---------- ---------- ---------- #

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._graph_descs = (
            _translate("Graph", "Double click here to open an image."),
            _translate("Graph", "Open"),
        )

        self._graph_errs = (
            _translate("Graph", "Error"),
            _translate("Graph", "Could not open image. Already has an image in process."),
            _translate("Graph", "Could not create temporary dir. Dir is not created."),
            _translate("Graph", "Could process image. Category is not match."),
        )

        self._image_descs = (
            _translate("Graph", "Finishing."),
            _translate("Graph", "Loading RGB data."),
            _translate("Graph", "Saving RGB data."),
            _translate("Graph", "Loading HSV data."),
            _translate("Graph", "Saving HSV data."),
            _translate("Graph", "Loading RGB vertical edge data."),
            _translate("Graph", "Saving RGB vertical edge data."),
            _translate("Graph", "Loading RGB horizontal edge data."),
            _translate("Graph", "Saving RGB horizontal edge data."),
            _translate("Graph", "Loading RGB final edge data."),
            _translate("Graph", "Saving RGB final edge data."),
            _translate("Graph", "Loading HSV vertical edge data."),
            _translate("Graph", "Saving HSV vertical edge data."),
            _translate("Graph", "Loading HSV horizontal edge data."),
            _translate("Graph", "Saving HSV horizontal edge data."),
            _translate("Graph", "Loading HSV final edge data."),
            _translate("Graph", "Saving HSV final edge data."),
        )
