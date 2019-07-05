# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QPixmap, QColor
from cguis.graph_view_form import Ui_graph_view
from clibs.trans2d import get_outer_box
import random
import numpy as np


class OverLabel(QLabel):
    """
    QLabel with color circles.
    """

    select_dist = 10
    st_color = (0, 0, 0)
    it_color = (0, 0, 0)
    pt_rtos = []
    pt_colors = []
    hm_rule = ""

    selected_pt_rtos = pyqtSignal(tuple)
    
    selecting = False

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.pt_rtos:
            lab_size = np.array((self.geometry().width(), self.geometry().height()), dtype=np.uint16)

            painter = QPainter()
            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            for i in range(5):
                pt_xy = self.pt_rtos[i] * lab_size
                pt_box = get_outer_box(pt_xy, self.select_dist)

                if self.pt_colors:
                    painter.setBrush(QColor(*self.pt_colors[i]))
                else:
                    painter.setBrush(QBrush(Qt.NoBrush))
                painter.setPen(QPen(QColor(*self.st_color), 2))
                painter.drawEllipse(*pt_box)

            for i in range(len(self.pt_rtos) - 5):
                pt_xy = self.pt_rtos[5 + i] * lab_size
                pt_box = get_outer_box(pt_xy, self.select_dist)

                if self.pt_colors:
                    painter.setBrush(QColor(*self.pt_colors[5 + i]))
                else:
                    painter.setBrush(QBrush(Qt.NoBrush))
                painter.setPen(QPen(QColor(*self.it_color), 2, Qt.PenStyle(Qt.DashLine)))
                painter.drawEllipse(*pt_box)

            painter.end()
    
    def mousePressEvent(self, event):
        lab_size = np.array((self.geometry().width(), self.geometry().height()), dtype=np.uint16)

        point = np.array((event.x(), event.y()))

        if self.hm_rule == "custom" and event.button() == Qt.LeftButton:
            for i in range(len(self.pt_rtos)):
                pt_xy = self.pt_rtos[i] * lab_size
                if np.linalg.norm(point - pt_xy) < self.select_dist:
                    self.pt_rtos.pop(i)
                    break
                
            pt_rto = (point / lab_size).astype(np.float32)

            pt_rto[0] = 0.0 if pt_rto[0] < 0.0 else pt_rto[0]
            pt_rto[0] = 1.0 if pt_rto[0] > 1.0 else pt_rto[0]
            pt_rto[1] = 0.0 if pt_rto[1] < 0.0 else pt_rto[1]
            pt_rto[1] = 1.0 if pt_rto[1] > 1.0 else pt_rto[1]
            
            self.pt_rtos = [pt_rto,] + self.pt_rtos

            while len(self.pt_rtos) < 5:
                self.pt_rtos.append(np.array((random.random(), random.random()), dtype=np.float32))

            self.selected_pt_rtos.emit(tuple(self.pt_rtos))
            self.selecting = True

            event.accept()
            self.update()

        elif event.button() == Qt.RightButton:
            clear_all = True
            for i in range(len(self.pt_rtos)):
                pt_xy = self.pt_rtos[i] * lab_size
                if np.linalg.norm(point - pt_xy) < self.select_dist * 1.2:
                    clear_all = False
                if np.linalg.norm(point - pt_xy) < self.select_dist:
                    self.pt_rtos.pop(i)
                    break
            
            if clear_all:
                self.pt_rtos = []
                self.pt_colors = []

            else:
                while len(self.pt_rtos) < 5:
                    self.pt_rtos.append(np.array((random.random(), random.random()), dtype=np.float32))

            self.selected_pt_rtos.emit(tuple(self.pt_rtos))

            event.accept()
            self.update()

        else:
            event.ignore()
    
    def mouseMoveEvent(self, event):
        if self.hm_rule == "custom" and self.selecting:
            lab_size = np.array((self.geometry().width(), self.geometry().height()), dtype=np.uint16)

            point = np.array((event.x(), event.y()))

            pt_rto = (point / lab_size).astype(np.float32)

            pt_rto[0] = 0.0 if pt_rto[0] < 0.0 else pt_rto[0]
            pt_rto[0] = 1.0 if pt_rto[0] > 1.0 else pt_rto[0]
            pt_rto[1] = 0.0 if pt_rto[1] < 0.0 else pt_rto[1]
            pt_rto[1] = 1.0 if pt_rto[1] > 1.0 else pt_rto[1]

            self.pt_rtos[0] = pt_rto

            self.selected_pt_rtos.emit(tuple(self.pt_rtos))

            event.accept()
            self.update()

        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            self.selecting = False

            event.accept()
            self.update()
        else:
            event.ignore()
    
    # ===== ===== ===== slot functions ===== ===== =====

    def slot_change_pt_rtos(self, pt_rtos):
        self.pt_rtos = list(pt_rtos) 
        self.update()
    
    def slot_set_colors(self, rgb_colors):
        self.pt_colors = rgb_colors
        self.update()

    def slot_set_hm_rule(self, hm_rule):
        self.hm_rule = hm_rule
        self.update()

    def slot_recover(self):
        self.selected_pt_rtos.emit(tuple(self.pt_rtos))
    
    def slot_clear_all(self):
        self.pt_rtos = []
        self.pt_colors = []


class View(QWidget, Ui_graph_view):
    """
    Graph view contain image, graph type and channel boxes.
    """

    selected_gph = pyqtSignal(int)
    selected_chl = pyqtSignal(int)

    def __init__(self, zoom_step, move_step, select_dist, st_color, it_color):
        """
        Init the graph view area.

        Parameters:
          setting - dict. setting environment.
        """
    
        super().__init__()
        self.setupUi(self)

        # loading settings.
        self.reload_settings(zoom_step, move_step, select_dist, st_color, it_color)

        # loading overlabel settings.
        self.graph_label = OverLabel(self)
        self.graph_label.setGeometry(0, 0, 1, 1)
        self.reload_overlabel()
        
        for name in ("gph", "chl"):
            cobox_name = getattr(self, "cobox_{}".format(name))
            cobox_name.raise_()
        
        for name in ("up", "down", "left", "right"):
            pbtn_move_name = getattr(self, "pbtn_move_{}".format(name))
            pbtn_move_name.raise_()
        
        for name in ("in", "out"):
            pbtn_zoom_name = getattr(self, "pbtn_zoom_{}".format(name))
            pbtn_zoom_name.raise_()
        
        self.pbtn_return_home.raise_()

        # once loaded.
        self._img = None

        # for zooming image.
        self._zoom = 1.0

        # for moving image.
        self._moving = False
        self._dist_x = 0
        self._dist_y = 0

        # set white background.
        palette = QPalette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        
        # emit graph type and channel co box value (to main graph).
        self.cobox_gph.currentIndexChanged.connect(lambda x: self.selected_gph.emit(self.cobox_gph.currentIndex()))
        self.cobox_chl.currentIndexChanged.connect(lambda x: self.selected_chl.emit(self.cobox_chl.currentIndex()))

        # set connection from zoom buttons to view.
        self.pbtn_zoom_in.clicked.connect(self.slot_zoom_in)
        self.pbtn_zoom_out.clicked.connect(self.slot_zoom_out)

        # set connection from home button to reset image.
        self.pbtn_return_home.clicked.connect(self.slot_reset_img)

        # set connection from move button to view.
        self.pbtn_move_up.clicked.connect(self.slot_move_up)
        self.pbtn_move_down.clicked.connect(self.slot_move_down)
        self.pbtn_move_left.clicked.connect(self.slot_move_left)
        self.pbtn_move_right.clicked.connect(self.slot_move_right)

    def reload_settings(self, zoom_step, move_step, select_dist, st_color, it_color):
        self._env_zoom_step = zoom_step
        self._env_move_step = move_step
        self._env_select_dist = select_dist
        self._env_st_color = st_color
        self._env_it_color = it_color

    def reload_overlabel(self):
        self.graph_label.select_dist = self._env_select_dist
        self.graph_label.st_color = self._env_st_color
        self.graph_label.it_color = self._env_it_color

    def reload_img(self):
        wid = self.geometry().width()
        hig = self.geometry().height()

        wid = 10 if wid < 10 else wid
        hig = 10 if hig < 10 else hig

        resized_img = self._img.scaled(wid, hig, Qt.KeepAspectRatio)
        img_wid = resized_img.size().width()
        img_hig = resized_img.size().height()
        self.graph_label.setGeometry((wid - img_wid) / 2, (hig - img_hig) / 2, img_wid, img_hig)
        self.graph_label.setPixmap(QPixmap.fromImage(resized_img))
        self.graph_label.show()

        self._zoom = 1.0

    def wheelEvent(self, event):
        point = (event.x(), event.y())

        ratio = (event.angleDelta() / 120).y()
        if ratio:
            ratio = ratio * self._env_zoom_step if ratio > 0 else -1 * ratio / self._env_zoom_step
        else:
            ratio = 1
        self._func_zoom_(point, ratio)

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            point = (event.x(), event.y())
            lab_x = self.graph_label.geometry().x()
            lab_y = self.graph_label.geometry().y()

            self._moving = True

            self._dist_x = lab_x - point[0]
            self._dist_y = lab_y - point[1]

            event.accept()
            self.update()

        else:
            # accept to prevent conflicts with graph events.
            event.accept()

    def mouseMoveEvent(self, event):
        point = (event.x(), event.y())

        if self._moving:
            self.graph_label.move(point[0] + self._dist_x, point[1] + self._dist_y)

            event.accept()
            self.update()

        else:
            # accept to prevent conflicts with graph events.
            event.accept()

    def mouseReleaseEvent(self, event):
        self._moving = False


    # ===== ===== ===== inner functions ===== ===== =====

    def _func_zoom_(self, center, ratio):
        """
        Zoom graphs.
        """

        wid = self.geometry().width()
        hig = self.geometry().height()
        local_center = center if center else (wid / 2, hig / 2)

        self._zoom *= ratio

        resized_img = self._img.scaled(wid * self._zoom, hig * self._zoom, Qt.KeepAspectRatio)
        img_wid = resized_img.size().width()
        img_hig = resized_img.size().height()

        lab_x = self.graph_label.geometry().x()
        lab_y = self.graph_label.geometry().y()

        z_lab_x = local_center[0] - ((local_center[0] - lab_x) * ratio)
        z_lab_y = local_center[1] - ((local_center[1] - lab_y) * ratio)

        self.graph_label.setGeometry(z_lab_x, z_lab_y, img_wid, img_hig)
        self.graph_label.setPixmap(QPixmap.fromImage(resized_img))

    def _func_move_(self, delta_x, delta_y):
        lab_x = self.graph_label.geometry().x()
        lab_y = self.graph_label.geometry().y()

        self.graph_label.move(lab_x + delta_x, lab_y + delta_y)


    # ===== ===== ===== slot functions ===== ===== =====

    def slot_change_gph(self, graph_type):
        if graph_type != self.cobox_gph.currentIndex():
            self.cobox_gph.setCurrentIndex(graph_type)
            self.update()

    def slot_change_chl(self, channel):
        if channel != self.cobox_chl.currentIndex():
            self.cobox_chl.setCurrentIndex(channel)
            self.update()
    
    def slot_load_img(self, img):
        self._img = img
        self.reload_img()
        self.update()
    
    def slot_zoom_in(self, value):
        self._func_zoom_(None, self._env_zoom_step)
        self.update()
    
    def slot_zoom_out(self, value):
        self._func_zoom_(None, 1 / self._env_zoom_step)
        self.update()

    def slot_reset_img(self, value):
        self.reload_img()

    def slot_move_up(self, value):
        self._func_move_(0, -1 * self._env_move_step)
    
    def slot_move_down(self, value):
        self._func_move_(0, self._env_move_step)
    
    def slot_move_left(self, value):
        self._func_move_(-1 * self._env_move_step, 0)
    
    def slot_move_right(self, value):
        self._func_move_(self._env_move_step, 0)
