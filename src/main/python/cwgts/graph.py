# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QImage
from clibs.trans2d import get_outer_box
from clibs.image3c import Image3C
from clibs.color import Color
from cwgts.view import View
import numpy as np


class Graph(QWidget):
    """
    Graph view frame.
    """

    selected_tr_color_0 = pyqtSignal(np.ndarray)
    selected_tr_color_1 = pyqtSignal(np.ndarray)
    selected_tr_color_2 = pyqtSignal(np.ndarray)
    selected_tr_color_3 = pyqtSignal(np.ndarray)
    selected_tr_color_4 = pyqtSignal(np.ndarray)

    selected_tr_hm_rule = pyqtSignal(str)

    def __init__(self, setting={}):
        """
        Init the graph work area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()

        self._env = {}
        self._env["hm_rule"] = setting["hm_rule"]
        self._env["vs_color"] = setting["vs_color"]
        self._env["auto_hide"] = setting["auto_hide"]
        self._env["tip_radius"] = setting["tip_radius"]
        self._env["temp_dir"] = setting["temp_dir"]
        self._env["graph_types"] = setting["graph_types"]
        self._env["graph_chls"] = setting["graph_chls"]
        self._env["half_sp"] = setting["half_sp"]
        self._env["zoom_step"] = setting["zoom_step"]
        self._env["move_step"] = setting["move_step"]
        self._env["select_dist"] = setting["select_dist"]
        self._env["st_color"] = setting["st_color"]
        self._env["it_color"] = setting["it_color"]

        self._label = QLabel(self)
        self._label.setText("Double click here to open a graph.")
        self._label.setWordWrap(True)

        self._image3c = Image3C(self._env)

        # graph views after image imported.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(self._env["half_sp"], self._env["half_sp"], self._env["half_sp"], self._env["half_sp"])
        grid_layout.setSpacing(self._env["half_sp"] * 2)
        self.setLayout(grid_layout)

        self._graph_views = []
        for i in range(4):
            graph_view = View(self._env)
            grid_layout.addWidget(graph_view, i // 2, i % 2, 1, 1)

            graph_view.hide()
            self._graph_views.append(graph_view)

            # init graph view type and channel.
            graph_view.slot_change_gph(self._env["graph_types"][i])
            graph_view.slot_change_chl(self._env["graph_chls"][i])
            
            # set connection from graph view type and channel to local setting.
            graph_view.selected_gph.connect(self.slot_change_gph(i))
            graph_view.selected_chl.connect(self.slot_change_chl(i))

        # set connections from one graph label to other graph labels and local graph colors.
        for i in range(4):
            from_graph_label = self._graph_views[i].graph_label

            for j in range(4):
                if j != i:
                    to_graph_label = self._graph_views[j].graph_label
                    from_graph_label.selected_pt_rtos.connect(to_graph_label.slot_change_pt_rtos)

            from_graph_label.selected_pt_rtos.connect(self.slot_set_graph_colors)

        self._image_imported = False    # image is opend.
        self._graph_changed = True      # changing graphs.
        self._ori_wid = 0               # original width.
        self._ori_hig = 0               # original height.
        self._ori_gph = [5, 5, 5, 5]    # original graph type. set 5 which doesn't exist for initialize.
        self._ori_chl = [5, 5, 5, 5]    # original channel. set 5 which doesn't exist for initialize.

        # for collecting selected colors in views.
        self._ref_graph = None  # referenced rgb data from import image.

        # for recover colors from wheel to graph interface.
        self._ori_colors = [np.array((0, 0, 0))] * 5
        
        # for func resize.
        self._pos_rto = np.array([0.5, 0.5])
        self._pos_moving = False

        # for func show.
        self._view_seq = [0, 1, 2, 3]

    def paintEvent(self, event):

        self._wid = self.geometry().width()
        self._hig = self.geometry().height()

        # paint analysis interface.
        if self._image_imported:
            self._label.hide()

            # draw tip circle.
            painter = QPainter()
            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            tip_center = np.array((self._wid, self._hig)) * self._pos_rto
            tip_box = get_outer_box(tip_center, self._env["tip_radius"])
            painter.setPen(QPen(QColor(*self._env["vs_color"]), 3))
            painter.setBrush(QBrush(Qt.NoBrush))
            
            painter.drawEllipse(*tip_box)
            painter.drawLine(tip_center[0], tip_center[1] + self._env["tip_radius"] * 0.4, tip_center[0], tip_center[1] - self._env["tip_radius"] * 0.4)
            painter.drawLine(tip_center[0] + self._env["tip_radius"] * 0.4, tip_center[1], tip_center[0] - self._env["tip_radius"] * 0.4, tip_center[1])

            painter.end()

            # update graph view sizes and contents.
            if self._wid != self._ori_wid or self._hig != self._ori_hig or self._graph_changed:
                self._func_show()
                self._func_resize_()
                self._func_update_view_()
                
                self._ori_wid = int(self._wid)
                self._ori_hig = int(self._hig)
                self._ori_gph = list(self._env["graph_types"])
                self._ori_chl = list(self._env["graph_chls"])
                
                self._graph_changed = False

        # paint open image interface.
        else:
            self._label.show()

            painter = QPainter()
            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            painter.setPen(QPen(Qt.black, Qt.PenStyle(Qt.DashLine), 3))
            painter.setBrush(Qt.white)
            box = (self._wid * 0.2, self._hig * 0.2, self._wid * 0.6, self._hig * 0.6)
            radius = min(self._wid * 0.1, self._hig * 0.1)
            painter.drawRoundedRect(*box, radius, radius)

            self._label.setGeometry(QRect(*box))
            self._label.setAlignment(Qt.AlignCenter)

            painter.end()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if not self._image_imported:
                box = (self._wid * 0.2, self._hig * 0.2, self._wid * 0.6, self._hig * 0.6)

                if box[0] < p_x < (box[0] + box[2]) and box[1] < p_y < (box[1] + box[3]):
                    self._func_open_graph_()
                    
                    event.accept()
                    self.update()
                else:
                    event.ignore()
            else:
                event.ignore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            point = np.array((event.x(), event.y()))
            tip_center = np.array((self._wid, self._hig)) * self._pos_rto

            if np.linalg.norm(point - tip_center) < self._env["tip_radius"]:
                pos_rto = point / np.array((self._wid, self._hig))
                pos_rto, show_list = self._func_pos_absorp_(pos_rto)
                self._pos_moving = True

                if (np.abs(pos_rto - self._pos_rto) > 1E-4).any():
                    self._pos_rto = pos_rto
                    self._view_seq = show_list
                    self._graph_changed = True

                    event.accept()
                    self.update()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseMoveEvent(self, event):
        if self._pos_moving:
            point = np.array((event.x(), event.y()))
            pos_rto = point / np.array((self._wid, self._hig))
            pos_rto, show_list = self._func_pos_absorp_(pos_rto)

            if (np.abs(pos_rto - self._pos_rto) > 1E-4).any():
                self._pos_rto = pos_rto
                self._view_seq = show_list
                self._graph_changed = True

                event.accept()
                self.update()
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._pos_moving = False


    # ===== ===== ===== inner functions ===== ===== =====
    
    def _func_open_graph_(self):
        """
        Slot func. Import a graph by double click label.
        """

        cb_file = QFileDialog.getOpenFileName(filter="All Graphs (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; \
                                                      PNG Graph (*.png);; \
                                                      BMP Graph (*.bmp);; \
                                                      JPEG Graph (*.jpg *.jpeg);; \
                                                      TIFF Graph (*.tif *.tiff);;")

        if cb_file[0]:
            self._ref_graph = self._image3c.import_image(cb_file[0])
            self._image_imported = True

    def _func_update_view_(self):
        """
        Update graph view.
        """

        for i in self._view_seq:
            if self._env["graph_types"][i] != self._ori_gph[i] or self._env["graph_chls"][i] != self._ori_chl[i]:
                img = self._image3c.load_image(self._env["graph_types"][i], self._env["graph_chls"][i])
                graph_view = self._graph_views[i]
                graph_view.slot_load_img(img)

    def _func_resize_(self):
        """
        Change view geometry size according to position ratio.
        """

        pos_x = int(self._wid * self._pos_rto[0])
        pos_y = int(self._hig * self._pos_rto[1])
        
        if self._graph_views[0].geometry().width() != (pos_x - self._env["half_sp"] * 2) or self._graph_views[0].geometry().height != (pos_y - self._env["half_sp"] * 2):
            if 0 in self._view_seq:
                self._graph_views[0].setGeometry(self._env["half_sp"], self._env["half_sp"], (pos_x - self._env["half_sp"] * 2), (pos_y - self._env["half_sp"] * 2))
            if 1 in self._view_seq:
                self._graph_views[1].setGeometry((pos_x + self._env["half_sp"]), self._env["half_sp"], (self._wid - pos_x - self._env["half_sp"] * 2), (pos_y - self._env["half_sp"] * 2))
            if 2 in self._view_seq:
                self._graph_views[2].setGeometry(self._env["half_sp"], (pos_y + self._env["half_sp"]), (pos_x -self._env["half_sp"] * 2), (self._hig - pos_y - self._env["half_sp"] * 2))
            if 3 in self._view_seq:
                self._graph_views[3].setGeometry((pos_x + self._env["half_sp"]), (pos_y + self._env["half_sp"]), (self._wid - pos_x - self._env["half_sp"] * 2), (self._hig - pos_y - self._env["half_sp"] * 2))

    def _func_show(self):
        """
        Change view visibility according to view sequence.
        """
        
        for i in range(4):
            if i in self._view_seq:
                self._graph_views[i].show()
            else:
                self._graph_views[i].hide()

    def _func_pos_absorp_(self, pos_rto):
        """
        The absorption of tip on special positions.
        """

        tip_wid = self._wid * pos_rto[0]
        tip_hig = self._hig * pos_rto[1]

        hide_list = [] # view hide list.

        if tip_wid < 50:
            pos_rto[0] = 0.0
            hide_list += [0, 2]
        elif self._wid - tip_wid < 50:
            pos_rto[0] = 1.0
            hide_list += [1, 3]
        
        if tip_hig < 50:
            pos_rto[1] = 0.0
            hide_list += [0, 1]
        elif self._hig - tip_hig < 50:
            pos_rto[1] = 1.0
            hide_list += [2, 3]
        
        if pos_rto[0] not in (0.0, 1.0) and pos_rto[1] not in (0.0, 1.0):
            if np.sqrt((tip_wid - self._wid / 2) ** 2 + (tip_hig - self._hig / 2) ** 2) < 30:
                pos_rto[0] = 0.5
                pos_rto[1] = 0.5
        
        if pos_rto[0] not in (0.0, 1.0) and pos_rto[1] in (0.0, 1.0):
            if np.sqrt((tip_wid - self._wid / 2) ** 2 + (tip_hig - pos_rto[1] * self._hig) ** 2) < 30:
                pos_rto[0] = 0.5
        
        if pos_rto[0] in (0.0, 1.0) and pos_rto[1] not in (0.0, 1.0):
            if np.sqrt((tip_wid - pos_rto[0] * self._wid) ** 2 + (tip_hig - self._hig / 2) ** 2) < 30:
                pos_rto[1] = 0.5

        show_list = [] # view show list (view seq).
        for i in range(4):
            if i not in hide_list:
                show_list.append(i)

        return pos_rto, tuple(show_list)


    # ===== ===== ===== slot functions ===== ===== =====

    def slot_reextract(self):
        """
        Slot func. Reextract color set.
        """

        self._func_open_graph_()

        self._ori_gph = [5, 5, 5, 5]
        self._ori_chl = [5, 5, 5, 5]

        for i in range(4):
            graph_label = self._graph_views[i].graph_label
            graph_label.slot_clear_all()

        self._graph_changed = True
        self.update()

    def slot_change_gph(self, graph_idx):
        """
        Slot func. Change graph type by co box.
        """

        def _func_(graph_type):
            if graph_type != self._env["graph_types"][graph_idx]:
                self._env["graph_types"][graph_idx] = graph_type

                self._graph_changed = True
                self.update()

        return _func_
    
    def slot_change_chl(self, graph_idx):
        """
        Slot func. Change channel by co box.
        """

        def _func_(channel):
            if channel != self._env["graph_chls"][graph_idx]:
                self._env["graph_chls"][graph_idx] = channel

                self._graph_changed = True
                self.update()

        return _func_

    def slot_update(self):
        """
        Update graph view when changing from wheel to graph in main loop. It would recover colors to None.
        """

        self._graph_changed = True

        if self._env["hm_rule"] == "custom":
            self._graph_views[0].graph_label.slot_recover()
        self.update()

    def slot_set_graph_colors(self, selected_rtos):
        """
        Use the first five colors in selected colors as result colors.
        """

        rgb_colors = []
        for selected_rto in selected_rtos:
            ref_size = np.array(self._ref_graph.shape[:2])
            ref_pos = (ref_size * selected_rto / 65535).astype(int)
            rgb = self._ref_graph[ref_pos[1]][ref_pos[0]]
            rgb_colors.append(rgb)
        
        for i in range(4):
            graph_label = self._graph_views[i].graph_label
            graph_label.slot_set_colors(rgb_colors)

        if rgb_colors:
            for i in range(5):
                selected_tr_color = getattr(self, "selected_tr_color_{}".format(i))
                selected_tr_color.emit(rgb_colors[i])

        self.update()

    def slot_set_hm_rule(self, hm_rule):
        """
        Slot func. Change current harmony rule.
        """

        def _func_(value):
            self._env["hm_rule"] = hm_rule

            for i in range(4):
                graph_label = self._graph_views[i].graph_label
                graph_label.slot_set_hm_rule(hm_rule)

            self.update()
        return _func_
