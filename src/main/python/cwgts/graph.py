# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage, QPalette
from clibs.color import Color
from clibs.trans2d import get_outer_box
from cguis.graph_views_form import Ui_graph_views
import numpy as np
from PIL import Image
import os


class Graph(QWidget, Ui_graph_views):
    def __init__(self, setting={}):
        """
        Init the graph work area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()
        self.setupUi(self)

        self._env = {}
        self._env["vs_color"] = setting["vs_color"]
        self._env["auto_hide"] = setting["auto_hide"]
        self._env["tip_radius"] = setting["tip_radius"]
        self._env["temp_dir"] = setting["temp_dir"]
        self._env["graph_types"] = setting["graph_types"]
        self._env["graph_chls"] = setting["graph_chls"]
        self._env["half_sp"] = setting["half_sp"]
        self._env["zoom_step"] = setting["zoom_step"]

        if not os.path.isdir(self._env["temp_dir"]):
            os.mkdir(self._env["temp_dir"])

        self._label = QLabel(self)
        self._label.setText("Double click here to open a graph.")
        self._label.setWordWrap(True)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(self._env["half_sp"], self._env["half_sp"], self._env["half_sp"], self._env["half_sp"])
        grid_layout.setSpacing(self._env["half_sp"] * 2)
        self.setLayout(grid_layout)

        for i in range(4):
            graph_view = getattr(self, "graph_view_{}".format(i))
            palette = QPalette()
            palette.setColor(self.backgroundRole(), Qt.white)
            graph_view.setPalette(palette)
            grid_layout.addWidget(graph_view, i // 2, i % 2, 1, 1)
            graph_view.hide()

            cobox_gph = getattr(self, "cobox_gph_{}".format(i))
            cobox_gph.setCurrentIndex(self._env["graph_types"][i])
            cobox_gph.currentIndexChanged.connect(self.slot_change_gph(i))

            cobox_chl = getattr(self, "cobox_chl_{}".format(i))
            cobox_chl.setCurrentIndex(self._env["graph_chls"][i])
            cobox_chl.currentIndexChanged.connect(self.slot_change_chl(i))

            pbtn_zoom_in = getattr(self, "pbtn_zoom_in_{}".format(i))
            pbtn_zoom_in.clicked.connect(self.slot_zoom(i, "i"))

            pbtn_zoom_out = getattr(self, "pbtn_zoom_out_{}".format(i))
            pbtn_zoom_out.clicked.connect(self.slot_zoom(i, "o"))

        self._image_imported = False    # image is opend.
        self._graph_changed = True      # changing graphs.
        self._init = True               # init graphs.
        self._ori_wid = 0               # original width.
        self._ori_hig = 0               # original height.
        self._ori_gph = [5, 5, 5, 5]    # original graph type.
        self._ori_chl = [5, 5, 5, 5]    # original channel.

        self._images = [None, None, None, None]

        self._zoom = [1.0, 1.0, 1.0, 1.0] # zoom size ratios.
        self._move_x = [0, 0, 0, 0]       # move offset.
        self._move_y = [0, 0, 0, 0]       # move offset.

        # for func resize.
        self._pos_rto = np.array([0.5, 0.5])
        self._pos_moving = False

        # for func show.
        self._view_seq = [0, 1, 2, 3]

    def paintEvent(self, event):
        self._wid = self.geometry().width()
        self._hig = self.geometry().height()
        self._box = (self._wid * 0.2, self._hig * 0.2, self._wid * 0.6, self._hig * 0.6)

        # paint analysis interface.
        if self._image_imported:
            self._label.hide()

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
            radius = min(self._wid * 0.1, self._hig * 0.1)
            painter.drawRoundedRect(*self._box, radius, radius)

            self._label.setGeometry(QRect(*self._box))
            self._label.setAlignment(Qt.AlignCenter)

            painter.end()
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if not self._image_imported:
                if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
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
    
    def wheelEvent(self, event):
        if self._image_imported:
            point = np.array((event.x(), event.y()))
            tip_center = np.array((self._wid, self._hig)) * self._pos_rto

            ratio = (event.angleDelta() / 120).y()
            if ratio:
                ratio = ratio * self._env["zoom_step"] if ratio > 0 else -1 * ratio / self._env["zoom_step"]
            else:
                ratio = 1


    # ===== ===== ===== inner functions ===== ===== =====

    def _func_import_image_(self, image_file):
        """
        Import a image from file and detect the H, S, V value edges of imported image.

        Parameters:
          image_file - string. image file path.
        """

        # import rgb data.
        rgb_data = np.array(Image.open(image_file).convert("RGB"), dtype=np.uint8)
        self._func_save_data_(rgb_data, "0")

        # transform from rgb to hsv.
        hsv_data = np.zeros(rgb_data.shape, dtype=np.uint16) # = hsv * 65535 (/ 360)

        for i in range(hsv_data.shape[0]):
            for j in range(hsv_data.shape[1]):
                hsv = Color.rgb_to_hsv(rgb_data[i][j])
                hsv = hsv / np.array((360.0, 1.0, 1.0)) * 65535
                hsv_data[i][j] = hsv.astype(np.uint16)

        # Sobel edge detection.
        results_shape = (hsv_data.shape[0] - 2, hsv_data.shape[1] - 2, 3)

        # vertical.
        vtl_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i][j + 2][0] + hsv_data[i + 1][j + 2][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i + 1][j][0] * 2 - hsv_data[i + 2][j][0]
                s_result = hsv_data[i][j + 2][1] + hsv_data[i + 1][j + 2][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i + 1][j][1] * 2 - hsv_data[i + 2][j][1]
                v_result = hsv_data[i][j + 2][2] + hsv_data[i + 1][j + 2][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i + 1][j][2] * 2 - hsv_data[i + 2][j][2]
                vtl_results[i][j] = np.array((abs(h_result) / 1028, abs(s_result) / 1028, abs(v_result) / 1028), dtype=np.uint8)

        # horizontal.
        hrz_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i + 2][j][0] + hsv_data[i + 2][j + 1][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i][j + 1][0] * 2 - hsv_data[i][j + 2][0]
                s_result = hsv_data[i + 2][j][1] + hsv_data[i + 2][j + 1][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i][j + 1][1] * 2 - hsv_data[i][j + 2][1]
                v_result = hsv_data[i + 2][j][2] + hsv_data[i + 2][j + 1][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i][j + 1][2] * 2 - hsv_data[i][j + 2][2]
                hrz_results[i][j] = np.array((abs(h_result) / 1028, abs(s_result) / 1028, abs(v_result) / 1028), dtype=np.uint8)

        # final.
        fnl_results = vtl_results + hrz_results

        self._func_save_data_(vtl_results, "1")
        self._func_save_data_(hrz_results, "2")
        self._func_save_data_(fnl_results, "3")

    def _func_read_channels_(self, rgb_data):
        """
        Read R, G, B part channels of rgb data.
        """

        r_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        g_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        b_channel = np.zeros(rgb_data.shape, dtype=np.uint8)

        for i in range(rgb_data.shape[0]):
            for j in range(rgb_data.shape[1]):
                r_channel[i][j][0] = rgb_data[i][j][0]
                g_channel[i][j][1] = rgb_data[i][j][1]
                b_channel[i][j][2] = rgb_data[i][j][2]
        
        return r_channel, g_channel, b_channel
    
    def _func_save_data_(self, rgb_data, prefix):
        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._env["temp_dir"] + os.sep + "{}_0.png".format(prefix))

        r_chl, g_chl, b_chl = self._func_read_channels_(rgb_data)

        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._env["temp_dir"] + os.sep + "{}_1.png".format(prefix))

        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._env["temp_dir"] + os.sep + "{}_2.png".format(prefix))

        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._env["temp_dir"] + os.sep + "{}_3.png".format(prefix))
    
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
            self._func_import_image_(cb_file[0])
            self._image_imported = True

    def _func_update_view_(self):
        """
        Update graph view.
        """

        for i in self._view_seq:
            if self._env["graph_types"][i] != self._ori_gph[i] or self._env["graph_chls"][i] != self._ori_chl[i]:
                img_name = "{}_{}.png".format(self._env["graph_types"][i], self._env["graph_chls"][i])
                img = QImage(self._env["temp_dir"] + os.sep + img_name)
                self._images[i] = img
                
            graph_view = getattr(self, "graph_view_{}".format(i))
            gph_wid = graph_view.geometry().width()
            gph_hig = graph_view.geometry().height()
            resized_img = self._images[i].scaled(gph_wid, gph_hig, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()
            graph_label = getattr(self, "graph_label_{}".format(i))
            graph_label.setGeometry((gph_wid - img_wid) / 2, (gph_hig - img_hig) / 2, img_wid, img_hig)
            graph_label.setPixmap(QPixmap.fromImage(resized_img))

    def _func_zoom_(self, idx, center, ratio):
        """
        Zoom graphs.
        """

        self._zoom[idx] *= ratio

        print(self._zoom[idx])

        graph_view = getattr(self, "graph_view_{}".format(idx))
        gph_wid = graph_view.geometry().width()
        gph_hig = graph_view.geometry().height()
        print(gph_wid, gph_hig)
        resized_img = self._images[idx].scaled(gph_wid * self._zoom[idx], gph_hig * self._zoom[idx], Qt.KeepAspectRatio)
        img_wid = resized_img.size().width()
        img_hig = resized_img.size().height()
        print(img_wid, img_hig)
        graph_label = getattr(self, "graph_label_{}".format(idx))
        lab_x = graph_label.geometry().x()
        lab_y = graph_label.geometry().y()
        print(lab_x, lab_y)
        z_lab_x = center[0] - ((center[0] - lab_x) * ratio)
        z_lab_y = center[1] - ((center[1] - lab_y) * ratio)
        print(z_lab_x, z_lab_y)
        graph_label.setGeometry(z_lab_x, z_lab_y, img_wid, img_hig)
        graph_label.setPixmap(QPixmap.fromImage(resized_img))

    def _func_move_(self):
        """
        Move graphs.
        """
        pass

        """
        for i in self._view_seq:
            self._graph_views[i].gview.items()[0].setOffset(self._move_x[i], self._move_y[i])
        """

    def _func_resize_(self):
        """
        Change view geometry size according to position ratio.
        """

        pos_x = int(self._wid * self._pos_rto[0])
        pos_y = int(self._hig * self._pos_rto[1])
        
        if self.graph_view_0.geometry().width() != (pos_x - self._env["half_sp"] * 2) or self.graph_view_0.geometry().height != (pos_y - self._env["half_sp"] * 2):
            if 0 in self._view_seq:
                self.graph_view_0.setGeometry(self._env["half_sp"], self._env["half_sp"], (pos_x - self._env["half_sp"] * 2), (pos_y - self._env["half_sp"] * 2))
            if 1 in self._view_seq:
                self.graph_view_1.setGeometry((pos_x + self._env["half_sp"]), self._env["half_sp"], (self._wid - pos_x - self._env["half_sp"] * 2), (pos_y - self._env["half_sp"] * 2))
            if 2 in self._view_seq:
                self.graph_view_2.setGeometry(self._env["half_sp"], (pos_y + self._env["half_sp"]), (pos_x -self._env["half_sp"] * 2), (self._hig - pos_y - self._env["half_sp"] * 2))
            if 3 in self._view_seq:
                self.graph_view_3.setGeometry((pos_x + self._env["half_sp"]), (pos_y + self._env["half_sp"]), (self._wid - pos_x - self._env["half_sp"] * 2), (self._hig - pos_y - self._env["half_sp"] * 2))

    def _func_show(self):
        """
        Change view visibility according to view sequence.
        """
        
        for i in range(4):
            graph_view = getattr(self, "graph_view_{}".format(i))
            if i in self._view_seq:
                graph_view.show()
            else:
                graph_view.hide()

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

        self._graph_changed = True
        self._ori_gph = [5, 5, 5, 5]
        self._ori_chl = [5, 5, 5, 5]

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
        Update graph view when changing from wheel to graph.
        """

        self._graph_changed = True
        self.update()

    def slot_move(self, idx, direction):
        """
        Move buttons.
        """

        def _func_(value):
            step = 50

            if direction == "u":
                self._move_y[idx] -= step
            elif direction == "d":
                self._move_y[idx] += step
            elif direction == "l":
                self._move_x[idx] -= step
            elif direction == "r":
                self._move_x[idx] += step
            else:
                raise ValueError("uexpect move direction: {}.".format(direction))
            
            self._gph_moving = True
            self.update()
        
        return _func_
    
    def slot_zoom(self, idx, direction):
        """
        Zoom buttons.
        """

        def _func_(value):
            if direction == "i":
                ratio = self._env["zoom_step"]
            elif direction == "o":
                ratio = 1 / self._env["zoom_step"]
            else:
                raise ValueError("uexpect zoom direction: {}.".format(direction))

            graph_view = getattr(self, "graph_view_{}".format(idx))
            self._func_zoom_(idx, (graph_view.size().width() / 2, graph_view.size().height() / 2), ratio)
            self.update()
        
        return _func_
