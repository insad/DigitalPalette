# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QTemporaryDir
from PyQt5.QtGui import QImage
from PIL import Image, ImageFilter
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
    ps_enhanced = pyqtSignal(int)

    def __init__(self):
        """
        Init image3c with default temp dir.
        """

        super().__init__()

        # load args.
        self._temp_dir = QTemporaryDir()

        self.run_image = None
        self.img_data = None
        self.display = None

        self.rgb_data = None
        self.hsv_data = None
        self.run_args = None
        self.run_category = None

        self._rgb_ext_data = None
        self._hsv_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None
        self._ori_display_data = None
        self._res_display_data = None

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def check_temp_dir(self):
        """
        Check if temporary directory valid.
        """

        return self._temp_dir.isValid() and os.path.isdir(self._temp_dir.path())

    def remove_temp_dir(self):
        """
        Remove temporary directory.
        """

        self._temp_dir.remove()

    def run(self):
        """
        Start running in thread.
        """

        if isinstance(self.run_category, int):
            func = getattr(self, "run_{}".format(self.run_category))
            func((0, 100))

        else:
            func = getattr(self, "run_{}".format(self.run_category))
            func((0, 100), self.run_args)

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

    def run_init(self, process_scope, script=""):
        """
        Run pre init data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
            script (str): (str): BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SHARPEN, SMOOTH, SMOOTH_MORE.
        """

        if isinstance(script, tuple) and script[0] in ("BLUR", "CONTOUR", "DETAIL", "EDGE_ENHANCE", "EDGE_ENHANCE_MORE", "EMBOSS", "FIND_EDGES", "SHARPEN", "SMOOTH", "SMOOTH_MORE"):
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))

            self.img_data = self.img_data.filter(getattr(ImageFilter, script[0]))

        elif isinstance(script, tuple) and script[0] == "ZOOM":
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))

            ratio = max(5.0 / self.img_data.size[0], 5.0 / self.img_data.size[1], script[1])

            if ratio != 1.0:
                self.img_data = self.img_data.resize((int(round(self.img_data.size[0] * ratio)), int(round(self.img_data.size[1] * ratio))), Image.ANTIALIAS)

        elif isinstance(script, tuple) and script[0] == "CROP":
            self.ps_describe.emit(17)
            self.ps_proceses.emit(int(process_scope[0]))

            if script[1] != (0.0, 0.0, 1.0, 1.0):
                self.img_data = self.img_data.crop((int(round(script[1][0] * self.img_data.size[0])), int(round(script[1][1] * self.img_data.size[1])), int(round(script[1][2] * self.img_data.size[0])), int(round(script[1][3] * self.img_data.size[1]))))

        else:
            self.ps_describe.emit(1)
            self.ps_proceses.emit(int(process_scope[0]))
            self.img_data = Image.open(self.run_image)

            ratio = max(5.0 / self.img_data.size[0], 5.0 / self.img_data.size[1])

            if ratio > 1.0:
                self.img_data = self.img_data.resize((int(self.img_data.size[0] * ratio), int(self.img_data.size[1] * ratio)), Image.ANTIALIAS)

        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.60))
        self.rgb_data = np.array(self.img_data.convert("RGB"), dtype=np.uint8)

        self.ps_proceses.emit(int(process_scope[0] + process_scope[1] * 0.80))
        self.save_rgb_full_data(self.rgb_data, 0)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(process_scope[0] + process_scope[1]))

    def run_0(self, process_scope):
        """
        Run normal rgb data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_init((process_scope[0], process_scope[1] * 0.40))
            pro_scope = (process_scope[0] + process_scope[1] * 0.40, process_scope[1] * 0.60)

        else:
            pro_scope = tuple(process_scope)

        # generating rgb data.
        self.ps_describe.emit(2)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.60))
        self.save_rgb_chnl_data(self.rgb_data, 0)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_4(self, process_scope):
        """
        Run normal hsv data.

        Args:
            process_scope (tuple or list): in format (start point, total length), e.g. (0, 100).
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.20))
            pro_scope = (process_scope[0] + process_scope[1] * 0.20, process_scope[1] * 0.80)

        else:
            pro_scope = tuple(process_scope)

        # generating hsv data.
        self.ps_describe.emit(3)
        self.ps_proceses.emit(int(pro_scope[0]))

        '''
        self.hsv_data = np.zeros(self.rgb_data.shape, dtype=np.float32)

        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.25))
        for i in range(self.hsv_data.shape[0]):
            for j in range(self.hsv_data.shape[1]):
                self.hsv_data[i][j] = Color.rgb2hsv(self.rgb_data[i][j])
        '''

        self.hsv_data = Color.rgb2hsv_array(self.rgb_data)

        self.ps_describe.emit(4)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.60))
        self.save_hsv_chnl_data(self.hsv_data, 4)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_1(self, process_scope):
        """
        Run vertical rgb space edge data.
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

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
                rgb_result = self._rgb_ext_data[i:i + 3, j:j + 3, :] * [[[-1, -1, -1], [0, 0, 0], [1, 1, 1]], [[-2, -2, -2], [0, 0, 0], [2, 2, 2]], [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]]
                rgb_result = rgb_result.sum(axis=(0, 1)) / 4

                self._rgb_vtl_data[i][j] = np.abs(rgb_result).astype(np.uint8)

        self.ps_describe.emit(6)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._rgb_vtl_data, 1)
        self.save_rgb_chnl_data(self._rgb_vtl_data, 1)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_2(self, process_scope):
        """
        Run horizontal rgb space edge data.
        """

        if not isinstance(self.rgb_data, np.ndarray):
            self.run_0((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        # get extended rgb data.
        self.run_rgb_extend()

        self.ps_describe.emit(7)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._rgb_hrz_data = np.zeros((self.rgb_data.shape[0], self.rgb_data.shape[1], 3), dtype=np.uint8)

        # generating rgb horizontal edge data.
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.40))
        for i in range(self.rgb_data.shape[0]):
            for j in range(self.rgb_data.shape[1]):
                rgb_result = self._rgb_ext_data[i:i + 3, j:j + 3, :] * [[[-1, -1, -1], [-2, -2, -2], [-1, -1, -1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[1, 1, 1], [2, 2, 2], [1, 1, 1]]]
                rgb_result = rgb_result.sum(axis=(0, 1)) / 4

                self._rgb_hrz_data[i][j] = np.abs(rgb_result).astype(np.uint8)

        self.ps_describe.emit(8)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._rgb_hrz_data, 2)
        self.save_rgb_chnl_data(self._rgb_hrz_data, 2)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_3(self, process_scope):
        """
        Run final rgb space edge data.
        """

        if not isinstance(self._rgb_vtl_data, np.ndarray):
            self.run_1((process_scope[0], process_scope[1] * 0.60))
            pro_scope = (process_scope[0] + process_scope[1] * 0.60, process_scope[1] * 0.40)

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
        self.save_rgb_full_data(fnl_results, 3)
        self.save_rgb_chnl_data(fnl_results, 3)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._rgb_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None

    def run_5(self, process_scope):
        """
        Run vertical hsv space edge data.
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        # get extended hsv data.
        self.run_hsv_extend()

        self.ps_describe.emit(11)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_vtl_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.uint8)

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

                sv_result = self._hsv_ext_data[i:i + 3, j:j + 3, 1:3] * [[[-1, -1], [0, 0], [1, 1]], [[-2, -2], [0, 0], [2, 2]], [[-1, -1], [0, 0], [1, 1]]]
                sv_result = sv_result.sum(axis=(0, 1)).astype(np.float32)

                self._hsv_vtl_data[i][j] = np.array((h_result * 0.3542, abs(sv_result[0]) * 63.75, abs(sv_result[1]) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(12)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._hsv_vtl_data, 5)
        self.save_rgb_chnl_data(self._hsv_vtl_data, 5)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_6(self, process_scope):
        """
        Run horizontal hsv space edge data.
        """

        if not isinstance(self.hsv_data, np.ndarray):
            self.run_4((process_scope[0], process_scope[1] * 0.35))
            pro_scope = (process_scope[0] + process_scope[1] * 0.35, process_scope[1] * 0.65)

        else:
            pro_scope = tuple(process_scope)

        # get extended hsv data.
        self.run_hsv_extend()

        self.ps_describe.emit(13)
        self.ps_proceses.emit(int(pro_scope[0]))
        self._hsv_hrz_data = np.zeros((self.hsv_data.shape[0], self.hsv_data.shape[1], 3), dtype=np.uint8)

        # generating hsv horizontal edge data.
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

                sv_result = self._hsv_ext_data[i:i + 3, j:j + 3, 1:3] * [[[-1, -1], [-2, -2], [-1, -1]], [[0, 0], [0, 0], [0, 0]], [[1, 1], [2, 2], [1, 1]]]
                sv_result = sv_result.sum(axis=(0, 1)).astype(np.float32)

                self._hsv_hrz_data[i][j] = np.array((h_result * 0.3542, abs(sv_result[0]) * 63.75, abs(sv_result[1]) * 63.75), dtype=np.uint8)

        self.ps_describe.emit(14)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1] * 0.80))
        self.save_rgb_full_data(self._hsv_hrz_data, 6)
        self.save_rgb_chnl_data(self._hsv_hrz_data, 6)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))

    def run_7(self, process_scope):
        """
        Run final hsv space edge data.
        """

        if not isinstance(self._hsv_vtl_data, np.ndarray):
            self.run_5((process_scope[0], process_scope[1] * 0.60))
            pro_scope = (process_scope[0] + process_scope[1] * 0.60, process_scope[1] * 0.40)

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
        self.save_rgb_full_data(fnl_results, 7)
        self.save_rgb_chnl_data(fnl_results, 7)

        self.ps_describe.emit(0)
        self.ps_proceses.emit(int(pro_scope[0] + pro_scope[1]))
        self._hsv_ext_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    def save_rgb_full_data(self, rgb_data, prefix):
        """
        Save rgb full channel image (0_0.png for category 0 and 4 and channel 0).
        """

        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._temp_dir.path() + os.sep + "{}_0.png".format(prefix))

        if prefix == 0:
            self.ps_finished.emit(0)
            self.ps_finished.emit(40)

        else:
            self.ps_finished.emit(prefix * 10)

    def save_rgb_chnl_data(self, rgb_data, prefix):
        """
        Save r, g, b channel images.
        """

        z_chl = np.zeros((rgb_data.shape[0], rgb_data.shape[1]), dtype=np.uint8)

        r_chl = np.stack((rgb_data[:, :, 0], z_chl, z_chl), axis=2)
        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 1)

        g_chl = np.stack((z_chl, rgb_data[:, :, 1], z_chl), axis=2)
        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 2)

        b_chl = np.stack((z_chl, z_chl, rgb_data[:, :, 1]), axis=2)
        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 3)

    def save_hsv_chnl_data(self, hsv_data, prefix):
        """
        Save h, s, v channel images.
        """

        '''
        h_channel = np.zeros(hsv_data.shape, dtype=np.uint8)
        s_channel = np.zeros(hsv_data.shape, dtype=np.uint8)
        v_channel = np.zeros(hsv_data.shape, dtype=np.uint8)

        for i in range(hsv_data.shape[0]):
            for j in range(hsv_data.shape[1]):
                h, s, v = hsv_data[i][j]
                h_channel[i][j] = Color.hsv2rgb((h, 1, 1))
                s_channel[i][j] = Color.hsv2rgb((0, s, 1))
                v_channel[i][j] = Color.hsv2rgb((0, 1, v))
        '''

        ones = np.ones(hsv_data.shape[:2])
        zeros = np.zeros(hsv_data.shape[:2])

        h_channel = Color.hsv2rgb_array(np.stack((hsv_data[:, :, 0], ones, ones), axis=2))
        s_channel = Color.hsv2rgb_array(np.stack((zeros, hsv_data[:, :, 1], ones), axis=2))
        v_channel = Color.hsv2rgb_array(np.stack((zeros, ones, hsv_data[:, :, 2]), axis=2))

        h_chl = QImage(h_channel, h_channel.shape[1], h_channel.shape[0], h_channel.shape[1] * 3, QImage.Format_RGB888)
        h_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 1)

        s_chl = QImage(s_channel, s_channel.shape[1], s_channel.shape[0], s_channel.shape[1] * 3, QImage.Format_RGB888)
        s_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 2)

        v_chl = QImage(v_channel, v_channel.shape[1], v_channel.shape[0], v_channel.shape[1] * 3, QImage.Format_RGB888)
        v_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 3)

    def load_image(self, category, channel):
        """
        Load image with category and channel.
        """

        if category in (0, 4) and channel == 0:
            img_path = os.sep.join((self._temp_dir.path(), "0_0.png"))

        else:
            img_path = os.sep.join((self._temp_dir.path(), "{}_{}.png".format(category, channel)))

        if os.path.isfile(img_path):
            img_data = Image.open(img_path).convert("RGB")
            self._ori_display_data = np.array(img_data, dtype=np.uint8)
            self.display = QImage(self._ori_display_data, self._ori_display_data.shape[1], self._ori_display_data.shape[0], self._ori_display_data.shape[1] * 3, QImage.Format_RGB888)

        else:
            self.display = None

    def run_enhance(self, process_scope, values):
        """
        Enhance rgb display by factor. Modify r, g or (and) b values to enhance the contrast of image.

        Args:
            values (tuple or list): (region, separation, factor, reserve)
        """

        reg, separ, fact, res = values

        if res and isinstance(self._res_display_data, np.ndarray):
            display_data = self._res_display_data

        else:
            display_data = np.array(self._ori_display_data, dtype=np.uint8)

            if res:
                self._res_display_data = display_data

            else:
                self._res_display_data = None

        separ = int(separ * 256)
        separ = 0 if separ < 0 else separ
        separ = 256 if separ > 256 else separ

        fact = float(fact)
        fact = 0.0 if fact < 0.0 else fact
        fact = 1.0 if fact > 1.0 else fact

        for k in reg:
            selection = np.where(display_data[:, :, k] >= separ)
            addi = np.array([0, 0, 0], dtype=np.uint8)
            addi[k] = 255 * fact

            display_data[:, :, k] = display_data[:, :, k] * (1 - fact)
            display_data[selection] += addi

            self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
            self.ps_enhanced.emit(0)

        self.ps_enhanced.emit(1)
