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
    """

    process = pyqtSignal(int)
    describe = pyqtSignal(int)
    ref_rgb = pyqtSignal(np.ndarray)
    finished = pyqtSignal(bool)

    def __init__(self):
        """
        Init image3c with default temp dir.
        """

        super().__init__()
        
        self._temp_dir = QTemporaryDir()
    
    def check_temp_dir(self):
        return self._temp_dir.isValid()
    
    def remove_temp_dir(self):
        self._temp_dir.remove()

    def import_image(self, image_file):
        """
        Import a image from file and detect the H, S, V value edges of imported image.
        Total steps = 4 + results_shape[0] + 1 + results_shape[0] + 1 + 3 + hsv_data.shape[0] + 2 + results_shape[0] + 1 + results_shape[0] + 1 + 1
                    = 6 + rgb_data.shape[0] * 5

        Parameters:
          image_file - string. image file path.

        Returns:
          np.ndarray. referenced rgb color.
        """

        self._image_file = image_file
    
    def run(self):
        # ===== ===== ===== RGB part ===== ===== =====

        # import rgb data.
        self.describe.emit(0)
        rgb_data = np.array(Image.open(self._image_file).convert("RGB"), dtype=np.uint8)
        self.ref_rgb.emit(rgb_data)
        self.process.emit(1)

        self.save_rgb_temp_data(rgb_data, "0")
        self.process.emit(2)

        # rgb space Sobel edge detection.
        self.describe.emit(1)
        results_shape = (rgb_data.shape[0] - 2, rgb_data.shape[1] - 2, 3)
        self.process.emit(3)

        next_process = 4

        # rgb vertical.
        self.describe.emit(2)
        vtl_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                r_result = rgb_data[i][j + 2][0] + rgb_data[i + 1][j + 2][0] * 2 + rgb_data[i + 2][j + 2][0] - rgb_data[i][j][0] - rgb_data[i + 1][j][0] * 2 - rgb_data[i + 2][j][0]
                g_result = rgb_data[i][j + 2][1] + rgb_data[i + 1][j + 2][1] * 2 + rgb_data[i + 2][j + 2][1] - rgb_data[i][j][1] - rgb_data[i + 1][j][1] * 2 - rgb_data[i + 2][j][1]
                b_result = rgb_data[i][j + 2][2] + rgb_data[i + 1][j + 2][2] * 2 + rgb_data[i + 2][j + 2][2] - rgb_data[i][j][2] - rgb_data[i + 1][j][2] * 2 - rgb_data[i + 2][j][2]
                vtl_results[i][j] = np.array((abs(r_result) / 4, abs(g_result) / 4, abs(b_result) / 4), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_rgb_temp_data(vtl_results, "1")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1
        
        # rgb horizontal.
        self.describe.emit(3)
        hrz_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                r_result = rgb_data[i + 2][j][0] + rgb_data[i + 2][j + 1][0] * 2 + rgb_data[i + 2][j + 2][0] - rgb_data[i][j][0] - rgb_data[i][j + 1][0] * 2 - rgb_data[i][j + 2][0]
                g_result = rgb_data[i + 2][j][1] + rgb_data[i + 2][j + 1][1] * 2 + rgb_data[i + 2][j + 2][1] - rgb_data[i][j][1] - rgb_data[i][j + 1][1] * 2 - rgb_data[i][j + 2][1]
                b_result = rgb_data[i + 2][j][2] + rgb_data[i + 2][j + 1][2] * 2 + rgb_data[i + 2][j + 2][2] - rgb_data[i][j][2] - rgb_data[i][j + 1][2] * 2 - rgb_data[i][j + 2][2]
                hrz_results[i][j] = np.array((abs(r_result) / 4, abs(g_result) / 4, abs(b_result) / 4), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_rgb_temp_data(hrz_results, "2")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1

        # rgb final.
        self.describe.emit(4)
        fnl_results = (np.sqrt(vtl_results.astype(np.uint32) ** 2 + hrz_results.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)
        self.process.emit(next_process)

        self.save_rgb_temp_data(fnl_results, "3")
        self.process.emit(next_process + 1)

        # ===== ===== ===== HSV part ===== ===== =====

        # transform from rgb to hsv.
        self.describe.emit(5)
        hsv_data = np.zeros(rgb_data.shape, dtype=np.float32) # = hsv * 1.0 (/ 360)
        self.process.emit(next_process + 2)

        next_process += 3

        for i in range(hsv_data.shape[0]):
            for j in range(hsv_data.shape[1]):
                h, s, v = Color.rgb_to_hsv(rgb_data[i][j])
                hsv_data[i][j] = np.array((h / 360.0, s, v), dtype=np.float32)

            self.process.emit(next_process + i)
        
        next_process += hsv_data.shape[0]

        self.save_hsv_temp_data(hsv_data, "4")
        self.process.emit(next_process)

        # hsv space Sobel edge detection.
        self.describe.emit(6)
        results_shape = (hsv_data.shape[0] - 2, hsv_data.shape[1] - 2, 3)
        self.process.emit(next_process + 1)

        next_process += 2

        # hsv vertical.
        self.describe.emit(7)
        vtl_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i][j + 2][0] + hsv_data[i + 1][j + 2][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i + 1][j][0] * 2 - hsv_data[i + 2][j][0]
                s_result = hsv_data[i][j + 2][1] + hsv_data[i + 1][j + 2][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i + 1][j][1] * 2 - hsv_data[i + 2][j][1]
                v_result = hsv_data[i][j + 2][2] + hsv_data[i + 1][j + 2][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i + 1][j][2] * 2 - hsv_data[i + 2][j][2]

                # 510 = 255 * 2.0, 127.5 = 255 / 2.0.
                h_result = abs(h_result)
                h_result = 510.0 - h_result * 127.5 if h_result > 2.0 else h_result * 127.5
                vtl_results[i][j] = np.array((h_result, abs(s_result) * 63.75, abs(v_result) * 63.75), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_rgb_temp_data(vtl_results, "5")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1

        # hsv horizontal.
        self.describe.emit(8)
        hrz_results = np.zeros(results_shape, dtype=np.uint8)
        for i in range(results_shape[0]):
            for j in range(results_shape[1]):
                h_result = hsv_data[i + 2][j][0] + hsv_data[i + 2][j + 1][0] * 2 + hsv_data[i + 2][j + 2][0] - hsv_data[i][j][0] - hsv_data[i][j + 1][0] * 2 - hsv_data[i][j + 2][0]
                s_result = hsv_data[i + 2][j][1] + hsv_data[i + 2][j + 1][1] * 2 + hsv_data[i + 2][j + 2][1] - hsv_data[i][j][1] - hsv_data[i][j + 1][1] * 2 - hsv_data[i][j + 2][1]
                v_result = hsv_data[i + 2][j][2] + hsv_data[i + 2][j + 1][2] * 2 + hsv_data[i + 2][j + 2][2] - hsv_data[i][j][2] - hsv_data[i][j + 1][2] * 2 - hsv_data[i][j + 2][2]

                # 510 = 255 * 2.0, 127.5 = 255 / 2.0.
                h_result = abs(h_result)
                h_result = 510.0 - h_result * 127.5 if h_result > 2.0 else h_result * 127.5
                hrz_results[i][j] = np.array((h_result, abs(s_result) * 63.75, abs(v_result) * 63.75), dtype=np.uint8)
            self.process.emit(next_process + i)

        self.save_rgb_temp_data(hrz_results, "6")
        self.process.emit(next_process + results_shape[0])

        next_process += results_shape[0] + 1

        # hsv final.
        self.describe.emit(9)
        fnl_results = (np.sqrt(vtl_results.astype(np.uint32) ** 2 + hrz_results.astype(np.uint32) ** 2) / np.sqrt(2)).astype(np.uint8)
        self.process.emit(next_process)

        self.save_rgb_temp_data(fnl_results, "7")
        self.process.emit(next_process + 1)

        self.describe.emit(10)
        self.finished.emit(True)

    def read_rgb_channels(self, rgb_data):
        """
        Read R, G, B part channels of rgb data.
        """

        r_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        g_channel = np.zeros(rgb_data.shape, dtype=np.uint8)
        b_channel = np.zeros(rgb_data.shape, dtype=np.uint8)

        for i in range(rgb_data.shape[0]):
            for j in range(rgb_data.shape[1]):
                r_channel[i][j][0] = rgb_data[i][j][0].astype(np.uint8)
                g_channel[i][j][1] = rgb_data[i][j][1].astype(np.uint8)
                b_channel[i][j][2] = rgb_data[i][j][2].astype(np.uint8)
        
        return r_channel, g_channel, b_channel
    
    def save_rgb_temp_data(self, rgb_data, prefix):
        rgb = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3, QImage.Format_RGB888)
        rgb.save(self._temp_dir.path() + os.sep + "{}_0.png".format(prefix))

        r_chl, g_chl, b_chl = self.read_rgb_channels(rgb_data)

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
                h_channel[i][j] = Color.hsv_to_rgb((h * 360.0, 1, 1)).astype(np.uint8)
                s_channel[i][j] = Color.hsv_to_rgb((360.0, s, 1)).astype(np.uint8)
                v_channel[i][j] = Color.hsv_to_rgb((360.0, 1, v)).astype(np.uint8)
        
        h_chl = QImage(h_channel, h_channel.shape[1], h_channel.shape[0], h_channel.shape[1] * 3, QImage.Format_RGB888)
        h_chl.save(self._temp_dir.path() + os.sep + "{}_1.png".format(prefix))

        s_chl = QImage(s_channel, s_channel.shape[1], s_channel.shape[0], s_channel.shape[1] * 3, QImage.Format_RGB888)
        s_chl.save(self._temp_dir.path() + os.sep + "{}_2.png".format(prefix))

        v_chl = QImage(v_channel, v_channel.shape[1], v_channel.shape[0], v_channel.shape[1] * 3, QImage.Format_RGB888)
        v_chl.save(self._temp_dir.path() + os.sep + "{}_3.png".format(prefix))

    def load_image(self, graph_type, channel):
        """
        Load splited images.

        Parameters:
          graph type - int.
            0: normal rgb data;
            1: vertical rgb space edge data;
            2: horizontal rgb space edge data;
            3: final rgb space edge data;
            4: normal hsv data;
            5: vertical hsv space edge data;
            6: horizontal hsv space edge data;
            7: final hsv space edge data.
          channel - int.
            0: rgb or hsv full data.
            1: r or h channel data;
            2: g or s channel data;
            3: b or v channel data.
        """

        if graph_type == 4 and channel == 0:
            img_name = "0_0.png"
        else:
            img_name = "{}_{}.png".format(graph_type, channel)

        img = QImage(self._temp_dir.path() + os.sep + img_name)

        return img
