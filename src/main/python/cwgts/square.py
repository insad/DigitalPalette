# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from clibs.color import Color
import numpy as np


class Square(QWidget):
    """
    Square object based on QWidget. Init a color square in result's cube.
    
    selected_color_set is a pyqt signal contains current color set.
    """

    selected_r = pyqtSignal(int)
    selected_g = pyqtSignal(int)
    selected_b = pyqtSignal(int)

    selected_h = pyqtSignal(float)
    selected_s = pyqtSignal(float)
    selected_v = pyqtSignal(float)

    selected_hsv = pyqtSignal(np.ndarray)
    selected_hex = pyqtSignal(str)

    selected_active = pyqtSignal(bool) # to wheel.

    def __init__(self, settings):
        """
        Init the color square.

        Parameters:
          setting - dict. setting environment.
        """

        super().__init__()

        # loading settings.
        self.reload_settings(settings)

        self._color = Color()
        self._ori_color = Color(self._color)

        self._emit_rgb = False   # emit selected_r, selected_g, selected_b
        self._emit_hsv = False   # emit selected_h, selected_s, selected_v
        self._emit_color = False # emit selected_hsv.

        self._acitvated_state = False   # acitvate state.
        self._emit_activated = True     # emit selected_active to wheel.
        self._activated_on = True       # set False to deactive and remain color 0 for graph view.

    def reload_settings(self, settings):
        self._env_at_color = settings[12]
        self._env_ia_color = settings[13]
        self._env_widratio = settings[6]

    def paintEvent(self, event):
        wid = self.geometry().width()
        hig = self.geometry().height()
        rto = (1.0 - self._env_widratio) / 2
        self._box = (wid * rto, hig * rto, wid * self._env_widratio, hig * self._env_widratio)
        painter = QPainter()
        painter.begin(self)

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if self._activated_on and self._acitvated_state:
            painter.setPen(QPen(QColor(*self._env_at_color), 5))
        else:
            painter.setPen(QPen(QColor(*self._env_ia_color), 3))
        painter.setBrush(QColor(*self._color.rgb))
        painter.drawRect(*self._box)

        painter.end()

        if self._color != self._ori_color:
            if self._emit_rgb:
                self.selected_r.emit(self._color.r)
                self.selected_g.emit(self._color.g)
                self.selected_b.emit(self._color.b)
                self._emit_rgb = False

            if self._emit_hsv:
                self.selected_h.emit(self._color.h)
                self.selected_s.emit(self._color.s)
                self.selected_v.emit(self._color.v)
                self._emit_hsv = False

            if self._emit_color:
                self.selected_hsv.emit(self._color.hsv)
                self._emit_color = False

            self.selected_hex.emit(self._color.hex_code)

            self._ori_color = Color(self._color)

        if self._emit_activated:
            self.selected_active.emit(self._acitvated_state)
            self._emit_activated = False

    def mousePressEvent(self, event):
        if self._activated_on and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                self._acitvated_state = True
                self._emit_activated = True
                event.accept()
                self.update()
            else:
                event.ignore()
        else:
            event.ignore()

    def mouseDoubleClickEvent(self, event):
        if self._activated_on and event.button() == Qt.LeftButton:
            p_x = event.x()
            p_y = event.y()

            if self._box[0] < p_x < (self._box[0] + self._box[2]) and self._box[1] < p_y < (self._box[1] + self._box[3]):
                self._acitvated_state = True
                self._emit_activated = True

                _color = QColorDialog.getColor(QColor(*self._color.rgb))
                if _color.isValid():
                    self._color.rgb = (_color.red(), _color.green(), _color.blue())

                event.accept()
                self.update()
            else:
                event.ignore()
        else:
            event.ignore()

    # ===== ===== ===== slot functions ===== ===== =====

    def slot_wheel_change_active_state(self, state):
        """
        Slot func. Change square's activate state by wheel.
        Will not emit acitvated state to wheel (emit_activated = False).
        """

        if state != self._acitvated_state:
            self._acitvated_state = bool(state)

            self._emit_activated = False
            self.update()

    def slot_spbox_change_active_state(self, state):
        """
        Slot func. Change square's activate state by spin box.
        Will emit acitvated state to wheel (emit_activated = True).
        """

        if state != self._acitvated_state:
            self._acitvated_state = bool(state)

            self._emit_activated = True
            self.update()

    def slot_change_color(self, hsv):
        """
        Slot func. Change square's color (hsv).
        """

        if not self._color.hsv_eq(hsv, acr=1E-3):
            self._color.hsv = hsv

            self._emit_rgb = True
            self._emit_hsv = True
            self._emit_color = False
            self.update()
    
    def slot_change_graph_color(self, rgb):
        """
        Slot func. Change square's color by graph view colors (rgb).
        """

        if not self._color.rgb_eq(rgb):
            self._color.rgb = rgb

            self._emit_rgb = True
            self._emit_hsv = True
            self._emit_color = True
            self.update()

    def slot_change_rgb(self, tag):
        """
        Slot func. Change square's color by rgb tag. It would emit hsv color then.
        """

        assert tag in ("r", "g", "b")
        def _func_(value):
            if abs(value - self._color.getti(tag)) > 0:
                self._color.setti(tag, value)
                self._emit_rgb = False
                self._emit_hsv = True
                # keep similar with slot_change_hsv.
                self.selected_hsv.emit(self._color.hsv)
                self.update()
        return _func_

    def slot_change_hsv(self, tag):
        """
        Slot func. Change square's color by hsv tag. It would emit rgb color then.
        """

        assert tag in ("h", "s", "v")
        def _func_(value):
            if abs(value - self._color.getti(tag)) > 1E-3:
                self._color.setti(tag, value)
                self._emit_rgb = True
                self._emit_hsv = False
                # paint event would not triggered when rgb color not changed (even hsv changed).
                self.selected_hsv.emit(self._color.hsv)
                self.update()
        return _func_

    def slot_change_hex_code(self, hex_code):
        """
        Slot func. Change square's color by hex code.
        """

        try:
            pr_hex_code = Color.fmt_hex(hex_code)
            if pr_hex_code != self._color.hex_code:
                self._color.setti_hex_code(pr_hex_code)
                self._acitvated_state = True
                self._emit_activated = True
                self._emit_rgb = True
                self._emit_hsv = True
                self._emit_color = True
                self.update()
        except:
            pass

    def slot_active_on(self, state):
        """
        Only active color 0 (black edge) in graph views.
        
        Parameters:
          state - bool. True for graph view and False for wheel. 
        """

        self._activated_on = state
        self.update()
