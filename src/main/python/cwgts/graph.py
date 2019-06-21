# -*- coding: utf-8 -*-

from cguis.graph_work_form import Ui_graph_work
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage
import numpy as np
from clibs.color import Color
from PIL import Image
from clibs.trans2d import get_outer_box
import os


class Graph(QWidget, Ui_graph_work):
    def __init__(self, setting={}):
        """
        Init the graph work area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()
        self.setupUi(self)

        self._env = {}
        self._env["view_method"] = setting["view_method"]
        self._env["vs_color"] = setting["vs_color"]
        self._env["auto_hide"] = setting["auto_hide"]
        self._env["tip_radius"] = setting["tip_radius"]
        self._env["temp_dir"] = setting["temp_dir"]
        self._env["graph_types"] = setting["graph_types"]
        self._env["graph_chls"] = setting["graph_chls"]

        if not os.path.isdir(self._env["temp_dir"]):
            os.mkdir(self._env["temp_dir"])

        half_tip_color = Color(self._env["vs_color"], ctp="rgb")
        half_tip_color.s /= 2
        self._half_tip_color = half_tip_color.rgb

        self._label = QLabel(self)
        self._label.setText("Double click here to open a graph.")
        self._label.setWordWrap(True)

        self._graph_labels = []
        for i in range(4):
            graph_ctx = getattr(self, "graph_ctx_{}".format(i))
            graph_label = QLabel(graph_ctx)
            graph_label.setAlignment(Qt.AlignCenter)
            self._graph_labels.append(graph_label)

            grid_layout = QGridLayout()
            grid_layout.addWidget(graph_label)
            grid_layout.setContentsMargins(1, 1, 1, 1)
            graph_ctx.setLayout(grid_layout)

            graph = getattr(self, "graph_{}".format(i))
            graph.hide()

        self._first = True          # initialize graph views.
        self._imported = False      # image is opend.
        self._changed = False       # changing graph or view.
        self._ori_wid = 0           # original width.
        self._ori_hig = 0           # original height.

        # according to temporary files.
        self._graph_files = [None, None, None, None]

        graph_value = {"rgb": 0, "vtl": 1, "hrz": 2, "fnl": 3}
        channel_value = {4: 0, 0: 1, 1: 2, 2: 3}

        for i in range(4):
            # set connections from co box to graph types.
            cobox_gph = getattr(self, "cobox_gph_{}".format(i))
            cobox_gph.currentIndexChanged.connect(self.slot_change_graph_type(i))

            # setup graph type default values.
            cobox_gph.setCurrentIndex(graph_value[self._env["graph_types"][i]])
        
            # set connections from co box to channels.
            cobox_chl = getattr(self, "cobox_chl_{}".format(i))
            cobox_chl.currentIndexChanged.connect(self.slot_change_channel(i))

            # setup channel default values.
            cobox_chl.setCurrentIndex(channel_value[self._env["graph_chls"][i]])

        # for func update.
        self._view_seq = {"individual": (0,), "referential": (0, 1,), "overall": (0, 1, 2, 3,)}
        self._x_y_pos_rto = {"individual": (1.0, 1.0), "referential": (0.5, 1.0), "overall": (0.5, 0.5)}

    def paintEvent(self, event):
        self._wid = self.geometry().width()
        self._hig = self.geometry().height()
        self._box = (self._wid * 0.2, self._hig * 0.2, self._wid * 0.6, self._hig * 0.6)

        # paint analysis interface.
        if self._imported:
            if self._first:
                self._label.hide()
                self._func_review_()
                self._first = False

            if self._wid != self._ori_wid or self._hig != self._ori_hig or self._changed:
                self._func_resize_()
                self._func_update_()
                
                self._ori_wid = self._wid
                self._ori_hig = self._hig
                self._changed = False
        
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

            if not self._imported:
                if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                    self._func_open_graph_()
                    
                    event.accept()
                    self.update()
                else:
                    event.ignore()
            else:
                event.ignore()


    # ===== ===== ===== inner functions ===== ===== =====

    def _func_import_image_(self, image_file):
        """
        Import a image from file and detect the H, S, V value edges of imported image.

        Parameters:
          image_file - string. image file path.
        """

        # import rgb data.
        rgb_data = np.array(Image.open(image_file).convert("RGB"), dtype=np.uint8)
        self._func_save_data_(rgb_data, "rgb")

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

        self._func_save_data_(vtl_results, "vtl")
        self._func_save_data_(hrz_results, "hrz")
        self._func_save_data_(fnl_results, "fnl")

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
        rgb.save(self._env["temp_dir"] + os.sep + "{}_4.png".format(prefix))

        r_chl, g_chl, b_chl = self._func_read_channels_(rgb_data)

        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._env["temp_dir"] + os.sep + "{}_0.png".format(prefix))

        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._env["temp_dir"] + os.sep + "{}_1.png".format(prefix))

        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._env["temp_dir"] + os.sep + "{}_2.png".format(prefix))
    
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
            self._imported = True

    def _func_update_(self):
        for i in range(4):
            graph_ctx = getattr(self, "graph_ctx_{}".format(i))

            if i in self._view_seq[self._env["view_method"]]:
                if self._graph_files[i] == None:
                    img_name = "{}_{}.png".format(self._env["graph_types"][i], self._env["graph_chls"][i])
                    self._graph_files[i] = QImage(self._env["temp_dir"] + os.sep + img_name)
                
                resized_img = self._graph_files[i].scaled(graph_ctx.geometry().width(), graph_ctx.geometry().height(), Qt.KeepAspectRatio)
                self._graph_labels[i].setPixmap(QPixmap.fromImage(resized_img))

    def _func_resize_(self):
        """
        Change view geometry size according to setting view method.
        """

        pos_x = self._wid * self._x_y_pos_rto[self._env["view_method"]][0]
        pos_y = self._hig * self._x_y_pos_rto[self._env["view_method"]][1]

        self.graph_0.setGeometry(0, 0, pos_x, pos_y)
        self.graph_1.setGeometry(pos_x, 0, self._wid - pos_x, pos_y)
        self.graph_2.setGeometry(0, pos_y, pos_x, self._hig - pos_y)
        self.graph_3.setGeometry(pos_x, pos_y, self._wid - pos_x, self._hig - pos_y)
    
    def _func_review_(self):
        """
        Change views visibility according to setting view method.
        """

        for i in range(4):
            graph = getattr(self, "graph_{}".format(i))
            if i in self._view_seq[self._env["view_method"]]:
                graph.show()
            else:
                graph.hide()


    # ===== ===== ===== slot functions ===== ===== =====

    def slot_change_view_method(self, method):
        """
        Slot func. Change the view method "individual", "referential" and "overall".
        """

        def _func_(value):
            if method != self._env["view_method"]:
                self._env["view_method"] = method
                self._func_review_()
                
                self._changed = True
                self.update()
        
        return _func_

    def slot_reextract(self):
        """
        Slot func. Reextract color set.
        """

        self._func_open_graph_()
        self._graph_files = [None, None, None, None]

        self._changed = True
        self.update()

    def slot_change_graph_type(self, graph_idx):
        """
        Slot func. Change graph type by co box.
        """

        def _func_(select_idx):
            value = {0: "rgb", 1: "vtl", 2: "hrz", 3: "fnl"}
            if value[select_idx] != self._env["graph_types"][graph_idx]:
                self._env["graph_types"][graph_idx] = value[select_idx]
                self._graph_files[graph_idx] = None

                self._changed = True
                self.update()

        return _func_
    
    def slot_change_channel(self, graph_idx):
        """
        Slot func. Change channel by co box.
        """

        def _func_(select_idx):
            value = {0: 4, 1: 0, 2: 1, 3: 2}
            if value[select_idx] != self._env["graph_chls"][graph_idx]:
                self._env["graph_chls"][graph_idx] = value[select_idx]
                self._graph_files[graph_idx] = None

                self._changed = True
                self.update()

        return _func_
    