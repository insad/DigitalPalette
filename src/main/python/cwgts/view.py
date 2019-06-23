# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QPixmap, QColor
from cguis.graph_view_form import Ui_graph_view
from clibs.trans2d import get_outer_box
import random


class View(QWidget, Ui_graph_view):
    """
    Graph view contain image, graph type and channel boxes.
    """

    selected_gph = pyqtSignal(int)
    selected_chl = pyqtSignal(int)

    selected_pt_rtos = pyqtSignal(tuple)

    def __init__(self, setting={}):
        """
        Init the graph view area.

        Parameters:
          setting - dict. setting environment.
        """
    
        super().__init__()
        self.setupUi(self)

        self._env = {}
        self._env["zoom_step"] = setting["zoom_step"]
        self._env["move_step"] = setting["move_step"]
        self._env["select_dist"] = setting["select_dist"]
        self._env["st_color"] = setting["st_color"]

        # once loaded.
        self._img = None
        self._img_loaded = False

        # for zooming image.
        self._zoom = 1.0

        # for moving image.
        self._moving = False
        self._dist_x = 0
        self._dist_y = 0

        # for selecting color.
        self._selecting = False
        self._pt_rtos = []

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

    def paintEvent(self, event):
        self._wid = self.geometry().width()
        self._hig = self.geometry().height()

        if self._img_loaded:
            resized_img = self._img.scaled(self._wid, self._hig, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()
            self.graph_label.setGeometry((self._wid - img_wid) / 2, (self._hig - img_hig) / 2, img_wid, img_hig)
            self.graph_label.setPixmap(QPixmap.fromImage(resized_img))

            self._zoom = 1.0
            self._img_loaded = False

        painter = QPainter()
        painter.begin(self)

        if self._pt_rtos:
            painter.setBrush(QBrush(Qt.NoBrush))
            painter.setPen(QPen(Qt.black, Qt.PenStyle(Qt.DashLine), 3))
            for pt_rto in self._pt_rtos[:-5]:
                _x = self.graph_label.geometry().x() + self.graph_label.geometry().width() * pt_rto[0]
                _y = self.graph_label.geometry().y() + self.graph_label.geometry().height() * pt_rto[1]

                _box = get_outer_box((_x, _y), self._env["select_dist"])
                painter.drawEllipse(*_box)

            painter.setPen(QPen(Qt.black, 3))
            for pt_rto in self._pt_rtos[-5:]:
                _x = self.graph_label.geometry().x() + self.graph_label.geometry().width() * pt_rto[0]
                _y = self.graph_label.geometry().y() + self.graph_label.geometry().height() * pt_rto[1]

                _box = get_outer_box((_x, _y), self._env["select_dist"])
                painter.drawEllipse(*_box)

        painter.end()

    def wheelEvent(self, event):
        point = (event.x(), event.y())

        ratio = (event.angleDelta() / 120).y()
        if ratio:
            ratio = ratio * self._env["zoom_step"] if ratio > 0 else -1 * ratio / self._env["zoom_step"]
        else:
            ratio = 1
        self._func_zoom_(point, ratio)
    
    def mousePressEvent(self, event):
        point = (event.x(), event.y())
        lab_x = self.graph_label.geometry().x()
        lab_y = self.graph_label.geometry().y()

        if event.button() == Qt.MidButton:
            self._moving = True

            self._dist_x = lab_x - point[0]
            self._dist_y = lab_y - point[1]

            event.accept()
            self.update()
        
        elif event.button() == Qt.LeftButton:
            rto_x = (point[0] - lab_x) / self.graph_label.geometry().width()
            rto_y = (point[1] - lab_y) / self.graph_label.geometry().height()

            if 0.0 < rto_x < 1.0 and 0.0 < rto_y < 1.0:
                for i in range(len(self._pt_rtos)):
                    if abs(rto_x - self._pt_rtos[i][0]) < self._env["select_dist"] and abs(rto_y - self._pt_rtos[i][1]) < self._env["select_dist"]:
                        self._pt_rtos.pop(i)
                        break
                
                self._pt_rtos.append((rto_x, rto_y))
                while len(self._pt_rtos) < 5:
                    self._pt_rtos = [(random.random(), random.random()),] + self._pt_rtos

                self.selected_pt_rtos.emit(tuple(self._pt_rtos))

                self._selecting = True

                event.accept()
                self.update()

            else:
                event.ignore()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        point = (event.x(), event.y())

        if self._moving:
            self.graph_label.move(point[0] + self._dist_x, point[1] + self._dist_y)

            event.accept()
            self.update()
        
        if self._selecting:
            rto_x = (point[0] - self.graph_label.geometry().x()) / self.graph_label.geometry().width()
            rto_y = (point[1] - self.graph_label.geometry().y()) / self.graph_label.geometry().height()

            rto_x = 0.0 if rto_x < 0.0 else rto_x
            rto_x = 1.0 if rto_x > 1.0 else rto_x
            rto_y = 0.0 if rto_y < 0.0 else rto_y
            rto_y = 1.0 if rto_y > 1.0 else rto_y

            self._pt_rtos[-1] = (rto_x, rto_y)
            self.selected_pt_rtos.emit(tuple(self._pt_rtos))

            event.accept()
            self.update()

    def mouseReleaseEvent(self, event):
        self._moving = False
        self._selecting = False


    # ===== ===== ===== inner functions ===== ===== =====

    def _func_zoom_(self, center, ratio):
        """
        Zoom graphs.
        """
        if self._img:
            self._zoom *= ratio

            resized_img = self._img.scaled(self._wid * self._zoom, self._hig * self._zoom, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()

            lab_x = self.graph_label.geometry().x()
            lab_y = self.graph_label.geometry().y()

            z_lab_x = center[0] - ((center[0] - lab_x) * ratio)
            z_lab_y = center[1] - ((center[1] - lab_y) * ratio)

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
        self._img_loaded = True
        self.update()
    
    def slot_zoom_in(self, value):
        center = (self._wid / 2, self._hig / 2)
        self._func_zoom_(center, self._env["zoom_step"])
        self.update()
    
    def slot_zoom_out(self, value):
        center = (self._wid / 2, self._hig / 2)
        self._func_zoom_(center, 1 / self._env["zoom_step"])
        self.update()

    def slot_reset_img(self, value):
        self._img_loaded = True

    def slot_move_up(self, value):
        self._func_move_(0, -1 * self._env["move_step"])
    
    def slot_move_down(self, value):
        self._func_move_(0, self._env["move_step"])
    
    def slot_move_left(self, value):
        self._func_move_(-1 * self._env["move_step"], 0)
    
    def slot_move_right(self, value):
        self._func_move_(self._env["move_step"], 0)

    def slot_change_pt_rtos(self, pt_rtos):
        self._pt_rtos = list(pt_rtos)
