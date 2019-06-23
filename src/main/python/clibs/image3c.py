# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage
from PIL import Image
from clibs.color import Color
import numpy as np
import os


class Image3C(object):
    """
    Image transformations.
    """

    def __init__(self, setting={}):
        """
        Init image3c with default temp dir.
        """

        self._env = {}
        self._env["temp_dir"] = setting["temp_dir"]

        if not os.path.isdir(self._env["temp_dir"]):
            os.makedirs(self._env["temp_dir"])

    def import_image(self, image_file):
        """
        Import a image from file and detect the H, S, V value edges of imported image.

        Parameters:
          image_file - string. image file path.
        """

        # import rgb data.
        rgb_data = np.array(Image.open(image_file).convert("RGB"), dtype=np.uint8)
        self.save_temp_data(rgb_data, "0")

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

        self.save_temp_data(vtl_results, "1")

        # horizontal.
        hrz_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i + 2][j][0] + hsv_data[i + 2][j + 1][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i][j + 1][0] * 2 - hsv_data[i][j + 2][0]
                s_result = hsv_data[i + 2][j][1] + hsv_data[i + 2][j + 1][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i][j + 1][1] * 2 - hsv_data[i][j + 2][1]
                v_result = hsv_data[i + 2][j][2] + hsv_data[i + 2][j + 1][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i][j + 1][2] * 2 - hsv_data[i][j + 2][2]
                hrz_results[i][j] = np.array((abs(h_result) / 1028, abs(s_result) / 1028, abs(v_result) / 1028), dtype=np.uint8)

        self.save_temp_data(hrz_results, "2")

        # final.
        fnl_results = vtl_results + hrz_results
        self.save_temp_data(fnl_results, "3")

    def read_channels(self, rgb_data):
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
    
    def save_temp_data(self, rgb_data, prefix):
        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._env["temp_dir"] + os.sep + "{}_0.png".format(prefix))

        r_chl, g_chl, b_chl = self.read_channels(rgb_data)

        r_chl = QImage(r_chl, r_chl.shape[1], r_chl.shape[0], r_chl.shape[1] * 3, QImage.Format_RGB888)
        r_chl.save(self._env["temp_dir"] + os.sep + "{}_1.png".format(prefix))

        g_chl = QImage(g_chl, g_chl.shape[1], g_chl.shape[0], g_chl.shape[1] * 3, QImage.Format_RGB888)
        g_chl.save(self._env["temp_dir"] + os.sep + "{}_2.png".format(prefix))

        b_chl = QImage(b_chl, b_chl.shape[1], b_chl.shape[0], b_chl.shape[1] * 3, QImage.Format_RGB888)
        b_chl.save(self._env["temp_dir"] + os.sep + "{}_3.png".format(prefix))

    def load_image(self, graph_type, channel):
        """
        Load splited images.
        
        Parameters:
          graph type - int. 0: normal rgb data; 1: vertical edge data; 2: horizontal edge data; 3: final edge data.
          channel - int. 0: rgb full data. 1: r channel data; 2: g channel data; 3: b channel data.
        """

        img_name = "{}_{}.png".format(graph_type, channel)
        img = QImage(self._env["temp_dir"] + os.sep + img_name)

        return img
