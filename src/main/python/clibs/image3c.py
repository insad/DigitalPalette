# -*- coding: utf-8 -*-

"""
DigitalPalette is a free software, which is distributed in the hope 
that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute 
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation. See the GNU General Public 
License for more details. 

Please visit https://liujiacode.github.io/DigitalPalette for more 
infomation about DigitalPalette.

Copyright © 2019-2020 by Eigenmiao. All Rights Reserved.
"""

import os
import random
import numpy as np
from PIL import Image, ImageFilter
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from clibs.color import Color


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

    Extract type:
        0: bright colorful
        1: light colorful
        2: dark colorful
        3: bright
        4: light
        5: dark
    """

    ps_proceses = pyqtSignal(int)
    ps_describe = pyqtSignal(int)
    ps_finished = pyqtSignal(int)
    ps_enhanced = pyqtSignal(int)
    ps_extracts = pyqtSignal(list)

    def __init__(self, temp_dir):
        """
        Init image3c with default temp dir.
        """

        super().__init__()

        # load args.
        self._temp_dir = temp_dir

        self.img_data = None
        self.display = None

        self.rgb_data = None
        self.hsv_data = None
        self.run_args = None
        self.run_category = None

        self.ori_display_data = None
        self.res_display_data = None
        self.rev_display_data = None

        self._rgb_ext_data = None
        self._hsv_ext_data = None
        self._rgb_vtl_data = None
        self._rgb_hrz_data = None
        self._hsv_vtl_data = None
        self._hsv_hrz_data = None

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

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

    def save_load_data(self, load_image):
        """
        Save load image from clipboard, etc.
        """

        i = 0
        image_path = self._temp_dir.path() + os.sep + "load_{}.png"
        while os.path.isfile(image_path.format(i)):
            i += 1

        image_path = image_path.format(i)

        try:
            load_image.save(image_path)

        except Exception as err:
            return None

        if os.path.isfile(image_path):
            return image_path

        else:
            return None

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

        ones = np.ones(hsv_data.shape[:2])
        zeros = np.zeros(hsv_data.shape[:2])

        h_chl = Color.hsv2rgb_array(np.stack((hsv_data[:, :, 0], ones, ones), axis=2))
        h_chl = QImage(h_chl, h_chl.shape[1], h_chl.shape[0], h_chl.shape[1] * 3, QImage.Format_RGB888)
        h_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 1)

        s_chl = Color.hsv2rgb_array(np.stack((zeros, hsv_data[:, :, 1], ones), axis=2))
        s_chl = QImage(s_chl, s_chl.shape[1], s_chl.shape[0], s_chl.shape[1] * 3, QImage.Format_RGB888)
        s_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))
        self.ps_finished.emit(prefix * 10 + 2)

        v_chl = Color.hsv2rgb_array(np.stack((zeros, ones, hsv_data[:, :, 2]), axis=2))
        v_chl = QImage(v_chl, v_chl.shape[1], v_chl.shape[0], v_chl.shape[1] * 3, QImage.Format_RGB888)
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
            try:
                img_data = Image.open(img_path).convert("RGB")
                self.ori_display_data = np.array(img_data, dtype=np.uint8)
                self.display = QImage(self.ori_display_data, self.ori_display_data.shape[1], self.ori_display_data.shape[0], self.ori_display_data.shape[1] * 3, QImage.Format_RGB888)

                self.res_display_data = self.ori_display_data
                self.rev_display_data = None

            except Exception as err:
                self.display = None

        else:
            self.display = None

    def run_enhance_rgb(self, process_scope, values):
        """
        Enhance rgb display by factor. Modify r, g or (and) b values to enhance the contrast of image.

        Args:
            values (tuple or list): (region, separation, factor, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, separ, fact, res, sigma = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        if isinstance(separ, (int, float)):
            separ = float(separ * 255.00001)
            separ = 0 if separ < 0 else separ
            separ = 255.00001 if separ > 255.00001 else separ
            separ = (separ, separ, separ)

        if isinstance(fact, (int, float)):
            fact = float(fact)
            fact = 0.0 if fact < 0.0 else fact
            fact = 1.0 if fact > 1.0 else fact
            fact = (fact, fact, fact)

        if isinstance(sigma, (int, float)):
            sigma = float(sigma)
            sigma = 0.0 if sigma < 0.0 else sigma
            sigma = 1.0 if sigma > 1.0 else sigma
            sigma = (sigma, sigma, sigma)

        for k in reg:
            data = display_data[:, :, k]
            selection = np.where(data >= separ[k])

            if sigma[k] == 0.0:
                expd = np.zeros(data.shape)
                expd[np.where(data == int(separ[k]))] = fact[k]

            elif sigma[k] == 1.0:
                expd = np.ones(data.shape) * fact[k]

            else:
                expd = 0.05 * (10 ** (10 * sigma[k])) * -1
                expd = np.exp((data - int(separ[k])) ** 2 / expd) * fact[k]

            data = data * (1 - expd)
            data[selection] = data[selection] + expd[selection] * 255

            display_data[:, :, k] = data

        self.res_display_data = display_data
        self.rev_display_data = None

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_enhance_hsv(self, process_scope, values):
        """
        Enhance hsv display by factor. Modify h, s or (and) v values to enhance the contrast of image.

        Args:
            values (tuple or list): (region, separation, factor, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, separ, fact, res, sigma = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        if isinstance(separ, (int, float)):
            separ = float(separ * 1.001)
            separ = 0.0 if separ < 0.0 else separ
            separ = 1.001 if separ > 1.001 else separ
            separ = (separ, separ, separ)

        if isinstance(fact, (int, float)):
            fact = float(fact)
            fact = 0.0 if fact < 0.0 else fact
            fact = 1.0 if fact > 1.0 else fact
            fact = (fact, fact, fact)

        if isinstance(sigma, (int, float)):
            sigma = float(sigma)
            sigma = 0.0 if sigma < 0.0 else sigma
            sigma = 1.0 if sigma > 1.0 else sigma
            sigma = (sigma, sigma, sigma)

        for k in reg:
            data = display_data[:, :, k]

            if sigma[k] == 0.0:
                expd = np.zeros(data.shape)
                expd[np.where((data < float(separ[k] + 1e-5)) & (data > float(separ[k] - 1e-5)))] = fact[k]

            elif sigma[k] == 1.0:
                expd = np.ones(data.shape) * fact[k]

            else:
                expd = 0.05 * (10 ** (10 * sigma[k])) * -1
                expd = np.exp((data - float(separ[k])) ** 2 / expd) * fact[k]

            if k == 0:
                data = data + expd * 360.0

            else:
                selection = np.where(data >= separ[k])

                data = data * (1 - expd)
                data[selection] = data[selection] + expd[selection]

            display_data[:, :, k] = data

        self.rev_display_data = display_data

        display_data = Color.hsv2rgb_array(display_data)

        self.res_display_data = display_data

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_inverse_rgb(self, process_scope, values):
        """
        Inverse rgb display. Modify r, g or (and) b values to inverse the contrast of image.

        Args:
            values (tuple or list): (region, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        for k in reg:
            display_data[:, :, k] = 255 - display_data[:, :, k]

        self.res_display_data = display_data
        self.rev_display_data = None

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_inverse_hsv(self, process_scope, values):
        """
        Inverse hsv display. Modify h, s or (and) v values to inverse the contrast of image.

        Args:
            values (tuple or list): (region, reserve).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        for k in reg:
            if k == 0:
                display_data[:, :, 0] = display_data[:, :, 0] + 180.0

            else:
                display_data[:, :, k] = 1.0 - display_data[:, :, k]

        self.rev_display_data = display_data

        display_data = Color.hsv2rgb_array(display_data)

        self.res_display_data = display_data

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_cover_rgb(self, process_scope, values):
        """
        Cover rgb display. Modify r, g or (and) b values to cover the channel of image.

        Args:
            values (tuple or list): (region, reserve, path).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res, path = values

        if res and isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = np.array(self.ori_display_data, dtype=np.uint8)

        if os.path.isfile(path):
            try:
                data = Image.open(path).convert("RGB")
                data = np.array(data, dtype=np.uint8)

                if data.shape == display_data.shape:
                    for k in reg:
                        display_data[:, :, k] = data[:, :, k]

                else:
                    self.ps_enhanced.emit(2)

            except Exception as err:
                self.ps_enhanced.emit(3)

        else:
            self.ps_enhanced.emit(3)

        self.res_display_data = display_data
        self.rev_display_data = None

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_cover_hsv(self, process_scope, values):
        """
        Cover hsv display. Modify h, s or (and) v values to cover the channel of image.

        Args:
            values (tuple or list): (region, reserve, path).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        reg, res, path = values

        if res and isinstance(self.rev_display_data, np.ndarray):
            display_data = self.rev_display_data

        elif res and isinstance(self.res_display_data, np.ndarray):
            display_data = Color.rgb2hsv_array(self.res_display_data)

        else:
            display_data = Color.rgb2hsv_array(self.ori_display_data)

        if os.path.isfile(path):
            try:
                data = Image.open(path).convert("RGB")
                data = np.array(data, dtype=np.uint8)

                if data.shape == display_data.shape:
                    data = Color.rgb2hsv_array(data)

                    for k in reg:
                        display_data[:, :, k] = data[:, :, k]

                else:
                    self.ps_enhanced.emit(2)

            except Exception as err:
                self.ps_enhanced.emit(3)

        else:
            self.ps_enhanced.emit(3)

        self.rev_display_data = display_data

        display_data = Color.hsv2rgb_array(display_data)

        self.res_display_data = display_data

        self.display = QImage(display_data, display_data.shape[1], display_data.shape[0], display_data.shape[1] * 3, QImage.Format_RGB888)
        self.ps_enhanced.emit(1)

    def run_extract(self, process_scope, values):
        """
        Cover hsv display. Modify h, s or (and) v values to cover the channel of image.

        Args:
            values (tuple or list): (random number, color type).
        """

        if not isinstance(self.ori_display_data, np.ndarray):
            return

        rand_num, color_type = values

        if isinstance(self.res_display_data, np.ndarray):
            display_data = self.res_display_data

        else:
            display_data = self.ori_display_data

        if rand_num > 0 and (display_data.shape[0] * display_data.shape[1]) > rand_num:
            data_pos = ((np.random.rand(rand_num) * display_data.shape[0]).astype(int), (np.random.rand(rand_num) * display_data.shape[1]).astype(int))
            data = display_data[data_pos]

        else:
            data = np.vstack(display_data)

        data_pos = np.where(np.logical_not(((data[:, 0] < 25) & (data[:, 1] < 25) & (data[:, 2] < 25)) | ((data[:, 0] > 225) & (data[:, 1] > 225) & (data[:, 2] > 225))))

        if len(data_pos[0]) > 120:
            data = data[data_pos]

        data = Color.rgb2hsv_array(np.array([data,]))[0]

        s_range = (data[:, 1].min(), data[:, 1].max())
        v_range = (data[:, 2].min(), data[:, 2].max())

        if color_type == 0:
            data_pos = np.where((data[:, 1] > s_range[0] + (s_range[1] - s_range[0]) * 0.1) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * 0.1))

        elif color_type == 1:
            data_pos = np.where((data[:, 1] < s_range[1] - (s_range[1] - s_range[0]) * 0.1) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * 0.1))

        elif color_type == 2:
            data_pos = np.where(data[:, 2] < v_range[1] - (v_range[1] - v_range[0]) * 0.1)

        elif color_type == 3:
            data_pos = np.where((data[:, 1] > s_range[0] + (s_range[1] - s_range[0]) * 0.2) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * 0.2))

        elif color_type == 4:
            data_pos = np.where((data[:, 1] < s_range[1] - (s_range[1] - s_range[0]) * 0.2) & (data[:, 2] > v_range[0] + (v_range[1] - v_range[0]) * 0.2))

        else:
            data_pos = np.where(data[:, 2] < v_range[1] - (v_range[1] - v_range[0]) * 0.2)

        if len(data_pos[0]) > 100:
            data = data[data_pos]

        data_samples = []
        s_samples = []
        v_samples = []
        extracts = []

        h_range = (data[:, 0].min(), data[:, 0].max())
        h_range = (h_range[0], h_range[1] - 1 / 12 * (h_range[1] - h_range[0]))

        for idx in range(5):
            mu = h_range[0] + (h_range[1] - h_range[0]) / 4 * idx
            sigma = (h_range[1] - h_range[0]) / 5

            for ext in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
                data_pos = np.where((data[:, 0] > (mu - sigma - ext * (mu - sigma - h_range[0]) - 1E-3)) & (data[:, 0] < (mu + sigma + ext * (h_range[1] - mu - sigma) + 1E-3)))

                if len(data_pos[0]) > 25:
                    break

            sample = data[data_pos]
            data_samples.append(sample)

            if color_type == 0:
                s_samples.append(sample[:, 1].max())
                v_samples.append(sample[:, 2].max())

            elif color_type == 1:
                s_samples.append(sample[:, 1].min())
                v_samples.append(sample[:, 2].max())

            elif color_type == 2:
                s_samples.append(sample[:, 1].min())
                v_samples.append(sample[:, 2].min())

            else:
                s_samples.append(0)
                v_samples.append(0)

        for idx in range(5):
            sample = data_samples[idx]

            s_range = (sample[:, 1].min(), sample[:, 1].max())
            v_range = (sample[:, 2].min(), sample[:, 2].max())

            if color_type == 0:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) / 5 * (5 - sorted(s_samples)[::-1].index(s_samples[idx]))
                v_mu = v_range[0] + (v_range[1] - v_range[0]) / 5 * (5 - sorted(v_samples)[::-1].index(v_samples[idx]))

            elif color_type == 1:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) / 5 * (4 - sorted(s_samples)[::-1].index(s_samples[idx]))
                v_mu = v_range[0] + (v_range[1] - v_range[0]) / 5 * (5 - sorted(v_samples)[::-1].index(v_samples[idx]))

            elif color_type == 2:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) * 0.5
                v_mu = v_range[0] + (v_range[1] - v_range[0]) / 5 * (4 - sorted(v_samples)[::-1].index(v_samples[idx]))

            elif color_type == 3:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) * 0.8
                v_mu = v_range[0] + (v_range[1] - v_range[0]) * 0.8

            elif color_type == 4:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) * 0.2
                v_mu = v_range[0] + (v_range[1] - v_range[0]) * 0.8

            else:
                s_mu = s_range[0] + (s_range[1] - s_range[0]) * 0.5
                v_mu = v_range[0] + (v_range[1] - v_range[0]) * 0.2

            s_sigma = (s_range[1] - s_range[0]) / 5
            v_sigma = (v_range[1] - v_range[0]) / 5

            for ext in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
                sample_pos = np.where((sample[:, 1] > (s_mu - s_sigma - ext * (s_mu - s_sigma - s_range[0]) - 1E-5)) & (sample[:, 1] < (s_mu + s_sigma + ext * (s_range[1] - s_mu - s_sigma) + 1E-5)) & (sample[:, 2] > (v_mu - v_sigma - ext * (v_mu - v_sigma - v_range[0]) - 1E-5)) & (sample[:, 2] < (v_mu + v_sigma + ext * (v_range[1] - v_mu - v_sigma) + 1E-5)))

                if len(sample_pos[0]) > 5:
                    break

            sample = sample[sample_pos]
            sample = sample[int(np.random.random() * sample.shape[0])]
            sample = Color.hsv2rgb(sample)

            sample_pos = np.where((display_data[:, :, 0] == sample[0]) & (display_data[:, :, 1] == sample[1]) & (display_data[:, :, 2] == sample[2]))

            if len(sample_pos[0]) < 1:
                sample_pos = np.where((display_data[:, :, 0] > sample[0] - 3) & (display_data[:, :, 0] < sample[0] + 3) & (display_data[:, :, 1] > sample[1] - 3) & (display_data[:, :, 1] < sample[1] + 3) & (display_data[:, :, 2] > sample[2] - 3) & (display_data[:, :, 2] < sample[2] + 3))

            pos = int(np.random.random() * len(sample_pos[0]))
            extracts.append((sample_pos[1][pos] / (display_data.shape[1] - 1), sample_pos[0][pos] / (display_data.shape[0] - 1)))

        self.ps_extracts.emit(extracts)
