# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QGridLayout, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QRect, pyqtSignal, QCoreApplication
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QPixmap, QImage
from cguis.resource import view_rc
from clibs.trans2d import get_outer_box
from clibs.image3c import Image3C
from cwgts.view import View
import numpy as np
import sys
import os


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

    def __init__(self, settings):
        """
        Init the graph work area.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()

        # loading settings.
        # graph types and graph chls are not allowed to reload.
        self.reload_settings(settings)
        self._env_graph_types = settings[18]
        self._env_graph_chls = settings[19]

        self._dbc_label = QLabel(self)
        self._dbc_label.setWordWrap(True)
        self._dbc_label.show()

        self._load_label = QLabel(self)
        self._load_label.hide()

        self._icon = QImage(":/images/images/icon_grey.png")
        self._icon_label = QLabel(self)
        self._icon_label.hide()

        self._image3c = Image3C()
        self._load_finished = True # loading finished. set False when loading.
        self._image3c.ref_rgb.connect(self.slot_set_ref_rgb)
        self._image3c.process.connect(self.slot_set_current_step)
        self._image3c.finished.connect(self.slot_set_loading_state)
        self._image3c.describe.connect(self.slot_set_loading_desc)

        # graph views after image imported.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(self._env_half_sp, self._env_half_sp, self._env_half_sp, self._env_half_sp)
        grid_layout.setSpacing(self._env_half_sp * 2)
        self.setLayout(grid_layout)

        self._pro_bar = QProgressBar() # loading process.
        self._pro_bar.setMaximum(100)
        self._pro_bar.setValue(0)
        grid_layout.addWidget(self._pro_bar, 3, 0, 1, 1)
        self._pro_bar.hide()

        self._graph_views = []
        for i in range(4):
            graph_view = View(self._env_zoom_step, self._env_move_step, self._env_select_dist, self._env_st_color, self._env_it_color)
            grid_layout.addWidget(graph_view, i // 2, i % 2, 1, 1)

            graph_view.hide()
            self._graph_views.append(graph_view)

            # init graph view type and channel.
            graph_view.slot_change_gph(self._env_graph_types[i])
            graph_view.slot_change_chl(self._env_graph_chls[i])
            
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

        # for collecting selected colors in views.
        self._ref_graph = None  # referenced rgb data from import image.

        # for func resize.
        self._pos_rto = np.array([0.5, 0.5])
        self._pos_moving = False
        self._tip_radius = 0

        # for func show.
        self._view_seq = [0, 1, 2, 3]

        # drop image.
        self.setAcceptDrops(True)
        self._accepted_file = ""

        # default path for importing and exporting.
        self._default_path = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette", "MyColors"))
        if not os.path.isdir(self._default_path):
            os.makedirs(self._default_path)

        # translate interface.
        self._func_tr_()

    def reload_settings(self, settings):
        self._env_hm_rule = settings[20]
        self._env_vs_color = settings[15]
        self._env_tip_radius = settings[5]
        self._env_half_sp = settings[11]
        self._env_zoom_step = settings[8]
        self._env_move_step = settings[9]
        self._env_select_dist = settings[10]
        self._env_st_color = settings[16]
        self._env_it_color = settings[17]
    
    def reload_view_settings(self):
        for graph_view in self._graph_views:
            graph_view.reload_settings(self._env_zoom_step, self._env_move_step, self._env_select_dist, self._env_st_color, self._env_it_color)
            graph_view.reload_overlabel()
        
        if self.isVisible():
            self._func_resize_()
            self.update()

    def paintEvent(self, event):
        self._wid = self.geometry().width()
        self._hig = self.geometry().height()

        # paint analysis interface.
        if self._image_imported and self._load_finished:
            # set tip radius.
            self._tip_radius = min(self._wid, self._hig) * self._env_tip_radius / 2

            # draw tip circle.
            painter = QPainter()
            painter.begin(self)

            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setRenderHint(QPainter.TextAntialiasing, True)
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

            tip_center = np.array((self._wid, self._hig)) * self._pos_rto
            
            tip_box = get_outer_box(tip_center, self._tip_radius)
            painter.setPen(QPen(QColor(*self._env_vs_color), 3))
            painter.setBrush(QBrush(Qt.NoBrush))
            
            painter.drawEllipse(*tip_box)
            painter.drawLine(tip_center[0], tip_center[1] + self._tip_radius * 0.4, tip_center[0], tip_center[1] - self._tip_radius * 0.4)
            painter.drawLine(tip_center[0] + self._tip_radius * 0.4, tip_center[1], tip_center[0] - self._tip_radius * 0.4, tip_center[1])

            painter.end()

            # update graph view sizes and contents.
            self._func_show_()
            self._func_resize_()

        # paint loading interface.
        elif self._image_imported and not self._load_finished:
            bar_wid = self._wid * 0.8
            bar_hig = self._hig * 0.1
            self._pro_bar.setGeometry((self._wid - bar_wid) / 2, self._hig - bar_hig * 1.2, bar_wid, bar_hig)
            
            resized_img = self._icon.scaled(self._wid * 0.8, self._hig * 0.8, Qt.KeepAspectRatio)
            img_wid = resized_img.size().width()
            img_hig = resized_img.size().height()

            self._icon_label.setPixmap(QPixmap.fromImage(resized_img))
            self._icon_label.setGeometry((self._wid - img_wid) / 2, bar_hig * 0.2, img_wid, img_hig)

            self._load_label.setGeometry((self._wid - bar_wid) / 2, self._hig - bar_hig * 2.2, bar_wid, bar_hig)

        # paint open image interface.
        else:
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

            self._dbc_label.setGeometry(QRect(*box))
            self._dbc_label.setAlignment(Qt.AlignCenter)

            painter.end()

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
        if event.button() == Qt.LeftButton and self._load_finished:
            point = np.array((event.x(), event.y()))
            tip_center = np.array((self._wid, self._hig)) * self._pos_rto

            if np.linalg.norm(point - tip_center) < self._tip_radius:
                pos_rto = point / np.array((self._wid, self._hig))
                pos_rto, show_list = self._func_pos_absorp_(pos_rto)
                self._pos_moving = True
                self.setCursor(Qt.SizeAllCursor)

                if (np.abs(pos_rto - self._pos_rto) > 1E-4).any():
                    self._pos_rto = pos_rto
                    self._view_seq = show_list

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

                event.accept()
                self.update()
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        self._pos_moving = False
        self.setCursor(Qt.ArrowCursor)

    def dragEnterEvent(self, event):
        image = event.mimeData().text()
        # ubuntu would add \r\n at end.
        image = image[:-2] if image[-2:] == "\r\n" else image
        image = image[:-1] if image[-1:] == "\n" else image
        
        if self._load_finished and image.split(".")[-1].lower() in ("png", "bmp", "jpg", "jpeg", "tif", "tiff") and image[:4] == "file":
            # ubuntu need / at start.
            self._accepted_file = image[8:] if sys.platform[:3].lower() == "win" else image[7:]
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if self._accepted_file:
            self.slot_open_image_file(self._accepted_file)
            self._accepted_file = ""
            event.accept()
        else:
            event.ignore()


    # ===== ===== ===== inner functions ===== ===== =====

    def _func_update_view_(self, idxes):
        """
        Update graph view.
        """

        for idx in idxes:
            img = self._image3c.load_image(self._env_graph_types[idx], self._env_graph_chls[idx])
            self._graph_views[idx].slot_load_img(img)

    def _func_resize_(self):
        """
        Change view geometry size according to position ratio.
        """

        pos_x = int(self._wid * self._pos_rto[0])
        pos_y = int(self._hig * self._pos_rto[1])
        
        if self._graph_views[0].geometry().width() != (pos_x - self._env_half_sp * 2) or self._graph_views[0].geometry().height != (pos_y - self._env_half_sp * 2):
            if 0 in self._view_seq:
                self._graph_views[0].setGeometry(self._env_half_sp, self._env_half_sp, (pos_x - self._env_half_sp * 2), (pos_y - self._env_half_sp * 2))
            if 1 in self._view_seq:
                self._graph_views[1].setGeometry((pos_x + self._env_half_sp), self._env_half_sp, (self._wid - pos_x - self._env_half_sp * 2), (pos_y - self._env_half_sp * 2))
            if 2 in self._view_seq:
                self._graph_views[2].setGeometry(self._env_half_sp, (pos_y + self._env_half_sp), (pos_x -self._env_half_sp * 2), (self._hig - pos_y - self._env_half_sp * 2))
            if 3 in self._view_seq:
                self._graph_views[3].setGeometry((pos_x + self._env_half_sp), (pos_y + self._env_half_sp), (self._wid - pos_x - self._env_half_sp * 2), (self._hig - pos_y - self._env_half_sp * 2))

    def _func_show_(self):
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

    def slot_open_graph(self, image=None):
        """
        Slot func. Import a graph by double click label.
        """
        if self._load_finished:
            cb_filter = "All Graphs (*.png *.bmp *.jpg *.jpeg *.tif *.tiff);; PNG Graph (*.png);; BMP Graph (*.bmp);; JPEG Graph (*.jpg *.jpeg);; TIFF Graph (*.tif *.tiff);;"
            cb_file = QFileDialog.getOpenFileName(None, self._dia_descs[0], self._default_path, filter=cb_filter)

            if cb_file[0]:
                self._default_path = os.path.dirname(cb_file[0])

                self.slot_open_image_file(cb_file[0])
        
        else:
            QMessageBox.warning(self, self._err_descs[0], self._err_descs[1])

    def slot_open_image_file(self, image):
        if self._image3c.check_temp_dir():
            for i in range(4):
                graph_label = self._graph_views[i].graph_label
                graph_label.slot_clear_all()

            self._image3c.import_image(image)
            self._image3c.start()

            self._dbc_label.hide()
            self._load_label.show()
            self._pro_bar.show()
            self._icon_label.show()
            self._view_seq = []
            self._func_show_()
            self._load_finished = False
            self._image_imported = True

            self.update()

        else:
            QMessageBox.warning(self, self._err_descs[0], self._err_descs[2])

    def slot_change_gph(self, graph_idx):
        """
        Slot func. Change graph type by co box.
        """

        def _func_(graph_type):
            self._env_graph_types[graph_idx] = graph_type
            self._func_update_view_((graph_idx,))

            self.update()

        return _func_
    
    def slot_change_chl(self, graph_idx):
        """
        Slot func. Change channel by co box.
        """

        def _func_(channel):
            self._env_graph_chls[graph_idx] = channel
            self._func_update_view_((graph_idx,))

            self.update()

        return _func_

    def slot_update(self):
        """
        Update graph view when changing from wheel to graph in main loop. It would recover colors to None.
        """

        if self._env_hm_rule == "custom":
            self._graph_views[0].graph_label.slot_recover()
        self.update()

    def slot_set_graph_colors(self, selected_rtos):
        """
        Use the first five colors in selected colors as result colors.
        """

        rgb_colors = []
        for selected_rto in selected_rtos:
            # length - 1 for array.
            ref_size = np.array(self._ref_graph.shape[:2]) - 1
            # the array x, y is different from image view x, y, which would cause an out-of-range error.
            ref_size[0], ref_size[1] = ref_size[1], ref_size[0]
            ref_pos = (ref_size * selected_rto).astype(int)
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
            self._env_hm_rule = hm_rule

            for i in range(4):
                graph_label = self._graph_views[i].graph_label
                graph_label.slot_set_hm_rule(hm_rule)

            self.update()
        return _func_

    def slot_set_current_step(self, step):
        """
        Getting current process.
        """

        self._pro_bar.setValue(step)
        self.update()

    def slot_set_ref_rgb(self, rgb_data):
        """
        Getting referenced graph.
        """

        self._ref_graph = rgb_data
        self._pro_bar.setMaximum(6 + rgb_data.shape[0] * 5)
        self.update()

    def slot_set_loading_state(self, state):
        """
        Loading finished process.
        """

        self._load_finished = True
        self._pro_bar.hide()
        self._icon_label.hide()
        self._load_label.hide()

        self._view_seq = [0, 1, 2, 3]
        self._func_resize_()
        self._func_update_view_(tuple(range(4)))
        self._func_show_()

        self.update()

    def slot_set_loading_desc(self, desc_idx):
        """
        Loading descriptions when importing a image.
        """

        self._load_label.setText(self._loading_descs[desc_idx])
        self._load_label.setAlignment(Qt.AlignCenter)
        self.update()

    def closeEvent(self, event):
        self._image3c.remove_temp_dir()

        event.accept()

    def _func_tr_(self):
        _translate = QCoreApplication.translate

        self._dbc_label.setText(
            _translate("Graph", "Double click here to open an image."),
        )

        self._loading_descs = (
            _translate("Graph", "Reading RGB data."),
            _translate("Graph", "Detecting image RGB space edges."),
            _translate("Graph", "Generating vertical RGB space edges."),
            _translate("Graph", "Generating horizontal RGB space edges."),
            _translate("Graph", "Integrating final RGB space edges."),
            _translate("Graph", "Transforming RGB to HSV data."),
            _translate("Graph", "Detecting image HSV space edges."),
            _translate("Graph", "Generating vertical HSV space edges."),
            _translate("Graph", "Generating horizontal HSV space edges."),
            _translate("Graph", "Integrating final HSV space edges."),
            _translate("Graph", "Finishing."),
        )

        self._err_descs = (
            _translate("Graph", "Error"),
            _translate("Graph", "Please open only one image in once time."),
            _translate("Graph", "Couldn't create temporary directory."),
        )

        self._dia_descs = (
            _translate("Graph", "Extract"),
        )
