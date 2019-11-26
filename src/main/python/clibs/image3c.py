# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QTemporaryDir
from PyQt5.QtGui import QImage
from PIL import Image
from clibs.color import Color
import numpy as np
import os


class Image3C(QThread):
    """
    Image transformations.

    Graph categories (finished signals):
        0: normal rgb data;
        1: vertical rgb space edge data;
        2: horizontal rgb space edge data;
        3: final rgb space edge data;
        4: normal hsv data;
        5: vertical hsv space edge data;
        6: horizontal hsv space edge data;
        7: final hsv space edge data.

    Graph channels:
        0: rgb or hsv full data.
        1: r or h channel data;
        2: g or s channel data;
        3: b or v channel data.
    """

    ps_proceses = pyqtSignal(int)
    ps_describe = pyqtSignal(int)
    ps_finished = pyqtSignal(int)

    def __init__(self):
        """
        Init image3c with default temp dir.
        """

        super().__init__()

        # load args.
        self._temp_dir = QTemporaryDir()

        self.run_image = None
        self.run_category = None
        self.rgb_data = None
        self.hsv_data = None

        self._rgb_ext_data = None
        self._hsv_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def initialize(self, image):
        self.run_image = image
        self.rgb_data = None
        self.hsv_data = None

        self._rgb_ext_data = None
        self._hsv_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    def check_temp_dir(self):
        return self._temp_dir.isValid()

    def remove_temp_dir(self):
        self._temp_dir.remove()

    def run(self):
        func = getattr(self, "run_{}".format(self.run_category))
        func((0, 100))

    def run_rgb_extend(self):
        """
        Extend rgb data into extended rgb data for Sobel edge detection.
        """

        if not isinstance(self._rgb_ext_data, np.ndarray):
            self._rgb_ext_data = np.insert(self.rgb_data, 0, self.rgb_data[1, :], axis=0)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, self._rgb_ext_data.shape[0], self._rgb_ext_data[self._rgb_ext_data.shape[0] - 2, :], axis=0)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, 0, self._rgb_ext_data[:, 1], axis=1)
            self._rgb_ext_data = np.insert(self._rgb_ext_data, self._rgb_ext_data.shape[1], self._rgb_ext_data[:, self._rgb_ext_data.shape[1] - 2], axis=1)

    def run_hsv_extend(self):
        """
        Extend rgb data into extended rgb data for Sobel edge detection.
        """

        if not isinstance(self._hsv_ext_data, np.ndarray):
            self._hsv_ext_data = np.insert(self.hsv_data, 0, self.hsv_data[1, :], axis=0)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, self._hsv_ext_data.shape[0], self._hsv_ext_data[self._hsv_ext_data.shape[0] - 2, :], axis=0)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, 0, self._hsv_ext_data[:, 1], axis=1)
            self._hsv_ext_data = np.insert(self._hsv_ext_data, self._hsv_ext_data.shape[1], self._hsv_ext_data[:, self._hsv_ext_data.shape[1] - 2], axis=1)

    def run_0(self, process_scope):
        """
        Run normal rgb data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        self.ps_describe.emit(1)
        self.ps_proceses.emit(int(process_scope[0]))
        img_data = Image.open(self.run_image).convert("RGB")

        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.25))
        self.rgb_data = np.array(img_data, dtype=np.uint8)

        # generating rgb data.
        self.ps_describe.emit(2)
        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.60))
        self.save_rgb_temp_data(self.rgb_data, 0)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(process_scope[0] + process_scope[1]))
        self.ps_finished.emit(0)

    def run_4(self, process_scope):
        """
        Run normal hsv data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.10))
            pro_scope = (process_scope[0] + process_scope[1] * 0.10, process_scope[1] * 0.90)

        else:
            pro_scope = tuple(process_scope)

        # generating hsv data.
        self.ps_describe.emit(3)
        self.ps_proceses.emit(int(pro_scope[0]))
        self.hsv_data = np.zeros(self.rgb_data.shape, dtype=np.float32)

        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.25))
        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                self.hsv_data[i][j] = Color.rgb2hsv(self.rgb_data[i][j])

        self.ps_describe.emit(4)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.60))
        self.save_hsv_temp_data(self.hsv_data, 4)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self.ps_finished.emit(4)

    def run_1(self, process_scope):
        """
        Run vertical rgb space edge data.
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        # get extended rgb data.
        self.run_rgb_extend()

        self.ps_describe.emit(5)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._rgb_vtl_data = np.zeros((self.rgb_data.shape[0], self.rgb_data.shape[1], 3), dtype=np.uint8)

        # generating rgb vertical edge data.
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))
        for i in range(self.rgb_data.shape[0]):
            for j in range(self.rgb_data.shape[1]):
                r_result = self._rgb_ext_data[i][j + 2][0] + self._rgb_ext_data[i + 1][j + 2][0] * 2 + self._rgb_ext_data[i + 2][j + 2][0] - self._rgb_ext_data[i][j][0] - self._rgb_ext_data[i + 1][j][0] * 2 - self._rgb_ext_data[i + 2][j][0]
                g_result = self._rgb_ext_data[i][j + 2][1] + self._rgb_ext_data[i + 1][j + 2][1] * 2 + self._rgb_ext_data[i + 2][j + 2][1] - self._rgb_ext_data[i][j][1] - self._rgb_ext_data[i + 1][j][1] * 2 - self._rgb_ext_data[i + 2][j][1]
                b_result = self._rgb_ext_data[i][j + 2][2] + self._rgb_ext_data[i + 1][j + 2][2] * 2 + self._rgb_ext_data[i + 2][j + 2][2] - self._rgb_ext_data[i][j][2] - self._rgb_ext_data[i + 1][j][2] * 2 - self._rgb_ext_data[i + 2][j][2]
                self._rgb_vtl_data[i][j] = np.array((abs(r_result) / 4, abs(g_result) / 4, abs(b_result) / 4), dtype=np.uint8)

        self.ps_describe.emit(6)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(self._rgb_vtl_data, 1)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self.ps_finished.emit(1)

    def run_2(self, process_scope):
        """
        Run horizontal rgb space edge data.
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        # get extended rgb data.
        self.run_rgb_extend()

        self.ps_describe.emit(7)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._rgb_hrz_data = np.zeros((self.rgb_data.shape[0], self.rgb_data.shape[1], 3), dtype=np.uint8)

        # generating rgb vertical edge data.
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))
        for i in range(self.rgb_data.shape[0]):
            for j in range(self.rgb_data.shape[1]):
                r_result = self._rgb_ext_data[i + 2][j][0] + self._rgb_ext_data[i + 2][j + 1][0] * 2 + self._rgb_ext_data[i + 2][j + 2][0] - self._rgb_ext_data[i][j][0] - self._rgb_ext_data[i][j + 1][0] * 2 - self._rgb_ext_data[i][j + 2][0]
                g_result = self._rgb_ext_data[i + 2][j][1] + self._rgb_ext_data[i + 2][j + 1][1] * 2 + self._rgb_ext_data[i + 2][j + 2][1] - self._rgb_ext_data[i][j][1] - self._rgb_ext_data[i][j + 1][1] * 2 - self._rgb_ext_data[i][j + 2][1]
                b_result = self._rgb_ext_data[i + 2][j][2] + self._rgb_ext_data[i + 2][j + 1][2] * 2 + self._rgb_ext_data[i + 2][j + 2][2] - self._rgb_ext_data[i][j][2] - self._rgb_ext_data[i][j + 1][2] * 2 - self._rgb_ext_data[i][j + 2][2]
                self._rgb_hrz_data[i][j] = np.array((abs(r_result) / 4, abs(g_result) / 4, abs(b_result) / 4), dtype=np.uint8)

        self.ps_describe.emit(8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(self._rgb_hrz_data, 2)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self.ps_finished.emit(2)

    def run_3(self, process_scope):
        """
        Run final rgb space edge data.
        """

        if not isinstance(self._rgb_vtl_data, np.ndarray):
            self.run_1((process_scope[0], process_scope[1] * 0.50))
            pro_scope = (process_scope[0] + process_scope[1] * 0.50, process_scope[1] * 0.50)

        else:
            pro_scope = tuple(process_scope)

        if not isinstance(self._rgb_hrz_data, np.ndarray):
            self.run_2((pro_scope[0], pro_scope[1] * 0.50))
            pro_scope = (pro_scope[0] + pro_scope[1] * 0.50, pro_scope[1] * 0.50)

        else:
            pro_scope = tuple(pro_scope)

        # generating rgb final edge data.
        self.ps_describe.emit(9)
        self.ps_proceses.emit(int(pro_scope[0]))
        fnl_results = (np.sqrt(self._rgb_vtl_data.astype(np.uint32) ** 2 + self._rgb_hrz_data.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)

        self.ps_describe.emit(10)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(fnl_results, 3)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self.ps_finished.emit(3)

    def run_5(self, process_scope):
        """
        Run vertical hsv space edge data.
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        # get extended hsv data.
        self.run_hsv_extend()

        self.ps_describe.emit(11)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_vtl_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.float32)

        # generating hsv vertical edge data.
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))
        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                h_result_0 = abs(self._hsv_ext_data[i + 0][j + 2][0] - self._hsv_ext_data[i + 0][j][0])
                h_result_1 = abs(self._hsv_ext_data[i + 1][j + 2][0] - self._hsv_ext_data[i + 1][j][0])
                h_result_2 = abs(self._hsv_ext_data[i + 2][j + 2][0] - self._hsv_ext_data[i + 2][j][0])
                h_result_0 = 360.0 - h_result_0 if h_result_0 > 180.0 else h_result_0
                h_result_1 = 360.0 - h_result_1 if h_result_1 > 180.0 else h_result_1
                h_result_2 = 360.0 - h_result_2 if h_result_2 > 180.0 else h_result_2
                h_result = h_result_0 + h_result_1 * 2 + h_result_2
                s_result = self._hsv_ext_data[i][j + 2][1] + self._hsv_ext_data[i + 1][j + 2][1] * 2 + self._hsv_ext_data[i + 2][j + 2][1] - self._hsv_ext_data[i][j][1] - self._hsv_ext_data[i + 1][j][1] * 2 - self._hsv_ext_data[i + 2][j][1]
                v_result = self._hsv_ext_data[i][j + 2][2] + self._hsv_ext_data[i + 1][j + 2][2] * 2 + self._hsv_ext_data[i + 2][j + 2][2] - self._hsv_ext_data[i][j][2] - self._hsv_ext_data[i + 1][j][2] * 2 - self._hsv_ext_data[i + 2][j][2]
                self._hsv_vtl_data[i][j] = np.array((h_result * 0.3542, abs(s_result) * 63.75, abs(v_result) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(12)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(self._hsv_vtl_data, 5)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self.ps_finished.emit(5)

    def run_6(self, process_scope):
        """
        Run horizontal hsv space edge data.
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        # get extended hsv data.
        self.run_hsv_extend()

        self.ps_describe.emit(13)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_hrz_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.float32)

        # generating hsv vertical edge data.
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))
        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                h_result_0 = abs(self._hsv_ext_data[i + 2][j + 0][0] - self._hsv_ext_data[i][j + 0][0])
                h_result_1 = abs(self._hsv_ext_data[i + 2][j + 1][0] - self._hsv_ext_data[i][j + 1][0])
                h_result_2 = abs(self._hsv_ext_data[i + 2][j + 2][0] - self._hsv_ext_data[i][j + 2][0])
                h_result_0 = 360.0 - h_result_0 if h_result_0 > 180.0 else h_result_0
                h_result_1 = 360.0 - h_result_1 if h_result_1 > 180.0 else h_result_1
                h_result_2 = 360.0 - h_result_2 if h_result_2 > 180.0 else h_result_2
                h_result = h_result_0 + h_result_1 * 2 + h_result_2
                s_result = self._hsv_ext_data[i + 2][j][1] + self._hsv_ext_data[i + 2][j + 1][1] * 2 + self._hsv_ext_data[i + 2][j + 2][1] - self._hsv_ext_data[i][j][1] - self._hsv_ext_data[i][j + 1][1] * 2 - self._hsv_ext_data[i][j + 2][1]
                v_result = self._hsv_ext_data[i + 2][j][2] + self._hsv_ext_data[i + 2][j + 1][2] * 2 + self._hsv_ext_data[i + 2][j + 2][2] - self._hsv_ext_data[i][j][2] - self._hsv_ext_data[i][j + 1][2] * 2 - self._hsv_ext_data[i][j + 2][2]
                self._hsv_hrz_data[i][j] = np.array((h_result * 0.3542, abs(s_result) * 63.75, abs(v_result) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(14)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(self._hsv_hrz_data, 6)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self.ps_finished.emit(6)

    def run_7(self, process_scope):
        """
        Run final hsv space edge data.
        """

        if not isinstance(self._hsv_vtl_data, np.ndarray):
            self.run_5((process_scope[0], process_scope[1] * 0.50))
            pro_scope = (process_scope[0] + process_scope[1] * 0.50, process_scope[1] * 0.50)

        else:
            pro_scope = tuple(process_scope)

        if not isinstance(self._hsv_hrz_data, np.ndarray):
            self.run_6((pro_scope[0], pro_scope[1] * 0.50))
            pro_scope = (pro_scope[0] + pro_scope[1] * 0.50, pro_scope[1] * 0.50)

        else:
            pro_scope = tuple(pro_scope)

        # generating rgb final edge data.
        self.ps_describe.emit(15)
        self.ps_proceses.emit(int(pro_scope[0]))
        fnl_results = (np.sqrt(self._hsv_vtl_data.astype(np.uint32) ** 2 + self._hsv_hrz_data.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)

        self.ps_describe.emit(16)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_temp_data(fnl_results, 7)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None
        self.ps_finished.emit(7)

    def save_rgb_temp_data(self, rgb_data, prefix):
        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._temp_dir.path() + os.sep + "{}_0.png".format(prefix))

        r_chl = np.zeros(rgb_data.shape, dtype=np.uint8)
        g_chl = np.zeros(rgb_data.shape, dtype=np.uint8)
        b_chl = np.zeros(rgb_data.shape, dtype=np.uint8)

        for i in range(rgb_data.shape[0]):
            for j in range(rgb_data.shape[1]):
                r_chl[i][j][0] = rgb_data[i][j][0]
                g_chl[i][j][1] = rgb_data[i][j][1]
                b_chl[i][j][2] = rgb_data[i][j][2]

        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))

        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))

        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))

    def save_hsv_temp_data(self, hsv_data, prefix):
        h_channel = np.zeros(hsv_data.shape, dtype=np.uint8)
        s_channel = np.zeros(hsv_data.shape, dtype=np.uint8)
        v_channel = np.zeros(hsv_data.shape, dtype=np.uint8)

        for i in range(hsv_data.shape[0]):
            for j in range(hsv_data.shape[1]):
                h, s, v = hsv_data[i][j]
                h_channel[i][j] = Color.hsv2rgb((h, 1, 1))
                s_channel[i][j] = Color.hsv2rgb((0, s, 1))
                v_channel[i][j] = Color.hsv2rgb((0, 1, v))

        h_chl = QImage(h_channel, h_channel.shape[1], h_channel.shape[0], h_channel.shape[1] * 3, QImage.Format_RGB888)
        h_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))

        s_chl = QImage(s_channel, s_channel.shape[1], s_channel.shape[0], s_channel.shape[1] * 3, QImage.Format_RGB888)
        s_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))

        v_chl = QImage(v_channel, v_channel.shape[1], v_channel.shape[0], v_channel.shape[1] * 3, QImage.Format_RGB888)
        v_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))

    def load_image(self, category, channel):
        """
        Load image with category and channel.
        """

        if category in (0, 4) and channel == 0:
            img_path = os.sep.join((self._temp_dir.path(), "0_0.png"))

        else:
            img_path = os.sep.join((self._temp_dir.path(), "{}_{}.png".format(category, channel)))

        if os.path.isfile(img_path):
            img = QImage(img_path)
            return img

        else:
            return None
