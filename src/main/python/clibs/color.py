# -*- coding: utf-8 -*-

import unittest
import numpy as np


class FakeColor(object):
    """
    FakeColor object. Storing rgb, hsv and hex code (hec) color without functional methods.
    """

    def __init__(self, rgb, hsv, hec):
        """
        Init FakeColor ojbect.

        Args:
            rgb (tuple or list): rgb color.
            rgb (tuple or list): hsv color.
            hec (str): hex code (hec).
        """

        self.rgb = Color.fmt_rgb(rgb)
        self.hsv = Color.fmt_hsv(hsv)
        self.hec = Color.fmt_hec(hec)

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def export(self):
        """
        Export color in dict type (for json file).

        Returns:
          color dict {"rgb": rgb_color_list, "hsv": hsv_color_list, "hex code": hex code (hec)}.
        """

        return {"rgb": self.rgb.tolist(), "hsv": self.hsv.tolist(), "hex code": self.hec}


class Color(object):
    """
    Color object. Storing rgb, hsv and hex code (hec) color.
    """

    def __init__(self, item, tp="color", overflow="cutoff"):
        """
        Init Color ojbect.

        Args:
            item (tuple, list, str or Color): rgb, hsv, hex code (hec) or another Color object.
            tp (str): type of color, in "rgb", "hsv", "hec" and "color".
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        self.set_overflow(overflow)

        if isinstance(tp, str) and tp in ("rgb", "hsv", "hec", "color"):
            self.setti(item, tp)

        else:
            raise ValueError("expect tp in str type and list 'rgb', 'hsv', 'hec' and 'color': {}.".format(tp))

    # ---------- ---------- ---------- Setting and Getting Funcs ---------- ---------- ---------- #

    def setti(self, item, tp):
        """
        Set color item.

        Args:
            item (tuple, list, str, int, float or Color): rgb, hsv, hex code (hec), r, g, b, h, s, v or another Color object.
            tp (str): type of color, in  "rgb", "hsv", "hec", "r", "g", "b", "h", "s", "v" and "color".
        """

        if not isinstance(tp, str):
            raise ValueError("expect tp in str type: {}.".format(tp))

        if tp.lower() == "color":
            if isinstance(item, (Color, FakeColor)):
                self._rgb, self._hsv, self._hec = self.fmt_rgb(item.rgb), self.fmt_hsv(item.hsv), self.fmt_hec(item.hec)

            else:
                raise ValueError("expect item in Color type: {}.".format(item))

        elif tp.lower() == "rgb":
            self._rgb = self.fmt_rgb(item)
            self._hsv = self.rgb2hsv(self._rgb)
            self._hec = self.rgb2hec(self._rgb)

        elif tp.lower() == "hsv":
            self._hsv = self.fmt_hsv(item, overflow=self._overflow)
            self._rgb = self.hsv2rgb(self._hsv)
            self._hec = self.hsv2hec(self._hsv)

        elif tp.lower() == "hec":
            self._hec = self.fmt_hec(item)
            self._rgb = self.hec2rgb(self._hec)
            self._hsv = self.hec2hsv(self._hec)

        elif tp.lower() == "r":
            rgb = list(self._rgb)
            rgb[0] = item
            self.setti(rgb, "rgb")

        elif tp.lower() == "g":
            rgb = list(self._rgb)
            rgb[1] = item
            self.setti(rgb, "rgb")

        elif tp.lower() == "b":
            rgb = list(self._rgb)
            rgb[2] = item
            self.setti(rgb, "rgb")

        elif tp.lower() == "h":
            hsv = list(self._hsv)
            hsv[0] = item
            self.setti(hsv, "hsv")

        elif tp.lower() == "s":
            hsv = list(self._hsv)
            hsv[1] = item
            self.setti(hsv, "hsv")

        elif tp.lower() == "v":
            hsv = list(self._hsv)
            hsv[2] = item
            self.setti(hsv, "hsv")

        else:
            raise ValueError("expect tp in list 'rgb', 'hsv', 'hec', 'r', 'g', 'b', 'h', 's', 'v' and 'color'.")

    def getti(self, tp):
        """
        Get color item.

        Args:
            tp (str): type of color, in  "rgb", "hsv", "hec", "r", "g", "b", "h", "s", "v" and "color".

        Returns:
            rgb, hsv, hex code (hec), r, g, b, h, s, v or another Color object.
        """

        if not isinstance(tp, str):
            raise ValueError("expect tp in str type: {}.".format(tp))

        if tp.lower() == "color":
            return Color(self)

        elif tp.lower() == "rgb":
            return tuple(self._rgb)

        elif tp.lower() == "hsv":
            return tuple(self._hsv)

        elif tp.lower() == "hec":
            return str(self._hec)

        elif tp.lower() == "r":
            return int(self._rgb[0])

        elif tp.lower() == "g":
            return int(self._rgb[1])

        elif tp.lower() == "b":
            return int(self._rgb[2])

        elif tp.lower() == "h":
            return float(self._hsv[0])

        elif tp.lower() == "s":
            return float(self._hsv[1])

        elif tp.lower() == "v":
            return float(self._hsv[2])

        else:
            raise ValueError("expect tp in list 'rgb', 'hsv', 'hec', 'r', 'g', 'b', 'h', 's', 'v' and 'color'.")

    def set_overflow(self, overflow):
        """
        Set the overflow method.

        Args:
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        if isinstance(overflow, str) and overflow in ("cutoff", "return", "repeat"):
            self._overflow = str(overflow)

        else:
            raise ValueError("expect value in str type and list 'cutoff', 'return', 'repeat': {}.".format(overflow))

    def get_overflow(self):
        """
        Get the overflow method.
        """

        return str(self._overflow)

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __str__(self):
        """
        Str format.
        """

        return "Color({}, {}, {})".format(self.r, self.g, self.b)

    def __repr__(self):
        """
        Repr format.
        """

        return "Color({}, {}, {}, {}, {}, {}, {})".format(self.r, self.g, self.b, self.h, self.s, self.v, self.hec)

    '''
    def __eq__(self, other):
        """
        Compare two colors by equal.

        Args:
            other (Color): another Color object for compare.

        Returns:
            True or False.
        """

        if isinstance(other, Color):
            return self._hec == other.hec
        else:
            raise ValueError("expect other in Color type: {}.".format(other))

    def __ne__(self, other):
        """
        Compare two colors by not equal.

        Args:
            other (Color): another Color object for compare.

        Returns:
            True or False.
        """

        if isinstance(other, Color):
            return self._hec != other.hec
        else:
            raise ValueError("expect other in Color type: {}.".format(other))
    '''

    # ---------- ---------- ---------- Properties and Setters ---------- ---------- ---------- #

    @property
    def rgb(self):
        return self.getti("rgb")

    @property
    def hsv(self):
        return self.getti("hsv")

    @property
    def hec(self):
        return self.getti("hec")

    @property
    def r(self):
        return self.getti("r")

    @property
    def g(self):
        return self.getti("g")

    @property
    def b(self):
        return self.getti("b")

    @property
    def h(self):
        return self.getti("h")

    @property
    def s(self):
        return self.getti("s")

    @property
    def v(self):
        return self.getti("v")

    @property
    def color(self):
        return self.getti("color")

    @rgb.setter
    def rgb(self, item):
        self.setti(item, "rgb")

    @hsv.setter
    def hsv(self, item):
        self.setti(item, "hsv")

    @hec.setter
    def hec(self, item):
        self.setti(item, "hec")

    @r.setter
    def r(self, item):
        self.setti(item, "r")

    @g.setter
    def g(self, item):
        self.setti(item, "g")

    @b.setter
    def b(self, item):
        self.setti(item, "b")

    @h.setter
    def h(self, item):
        self.setti(item, "h")

    @s.setter
    def s(self, item):
        self.setti(item, "s")

    @v.setter
    def v(self, item):
        self.setti(item, "v")

    @color.setter
    def color(self, item):
        self.setti(item, "color")

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def export(self):
        """
        Export color in dict type (for json file).

        Returns:
          color dict {"rgb": rgb_color_list, "hsv": hsv_color_list, "hex code": hex code (hec)}.
        """

        return {"rgb": self._rgb.tolist(), "hsv": self._hsv.tolist(), "hex code": self._hec}

    # ---------- ---------- ---------- Classmethods ---------- ---------- ---------- #

    @classmethod
    def fmt_rgb(cls, rgb):
        """
        Class method. Format item to standard rgb color.

        Args:
            rgb (tuple or list): color item to be formated.

        Returns:
            Standard rgb color.
        """

        if len(rgb) == 3:
            _rgb = np.rint(rgb)

            if (_rgb >= (0, 0, 0)).all() and (_rgb <= (255, 255, 255)).all():
                return _rgb.astype(np.uint8)

            else:
                raise ValueError("expect r, g, b in range 0 ~ 255: {}.".format(rgb))

        else:
            raise ValueError("expect rgb color in length 3: {}.".format(rgb))

    @classmethod
    def fmt_hsv(cls, hsv, overflow="cutoff"):
        """
        Class method. Format item to standard hsv color.

        Args:
            hsv (tuple or list): color item to be formated.
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".

        Returns:
            Standard hsv color.
        """

        if not isinstance(overflow, str):
            raise ValueError("expect overflow in str type: {}.".format(overflow))

        if len(hsv) == 3:
            _h, _s, _v = hsv

            if not (0.0 <= _s <= 1.0 and 0.0 <= _v <= 1.0):
                if overflow.lower() == "cutoff":
                    _s = 0.0 if _s < 0.0 else _s
                    _s = 1.0 if _s > 1.0 else _s
                    _v = 0.0 if _v < 0.0 else _v
                    _v = 1.0 if _v > 1.0 else _v

                elif overflow.lower() == "return":
                    _s = _s % 1.0 if _s // 1.0 % 2.0 == 0.0 else 1.0 - (_s % 1.0)
                    _v = _v % 1.0 if _v // 1.0 % 2.0 == 0.0 else 1.0 - (_v % 1.0)

                elif overflow.lower() == "repeat":
                    _s = _s % 1.0
                    _v = _v % 1.0

                else:
                    raise ValueError("expect overflow in list 'cutoff', 'return' and 'repeat'.")

            _h = round(_h % 360.0 * 1E5) / 1E5
            _s = round(_s * 1E5) / 1E5
            _v = round(_v * 1E5) / 1E5

            return np.array((_h, _s, _v), dtype=np.float32)

        else:
            raise ValueError("expect hsv color in length 3: {}.".format(hsv))

    @classmethod
    def fmt_hec(cls, hec):
        """
        Class method. Format item to standard hex code (hec) color.

        Args:
            hec (str): color item to be formated.

        Returns:
            Standard hex code (hec) color.
        """

        if not isinstance(hec, str):
            raise ValueError("expect hex code (hec) in str type: {}.".format(hec))

        if len(hec) == 6:
            for stri in hec.upper():
                if stri not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"):
                    raise ValueError("expect code in hex type: {}.".format(hec))

        else:
            raise ValueError("expect hex code (hec) in length 6: {}.".format(hec))

        return hec.upper()

    @classmethod
    def rgb2hsv(cls, rgb):
        """
        Translate rgb color into hsv color.

        Args:
            rgb (tuple or list): rgb color.

        Returns:
            hsv color.
        """

        color = cls.fmt_rgb(rgb)

        v = max(color) / 255.0
        if abs(v - 0) < 1E-5:
            color = np.array((255, 0, 0))

        else:
            color = color / v

        s = 1 - min(color) / 255.0
        if abs(s - 0) < 1E-5:
            color = np.array((255, 0, 0))

        else:
            color = (color - 255 * (1 - s)) / s
            color = np.rint(color).astype(int)

        if color[0] == 255:
            if color[2] == 0:
                # red to yellow, 0 to 60.
                h = color[1] / 255 * 60

            elif color[1] == 0:
                # magenta to red, 300 to 360.
                h = 360 - color[2] / 255 * 60

            else:
                raise ValueError("value 0 is not found in red area: {}.".format(color))

        elif color[1] == 255:
            if color[0] == 0:
                # green to cyan, 120 to 180.
                h = 120 + color[2] / 255 * 60

            elif color[2] == 0:
                # yellow to green, 60 to 120.
                h = 120 - color[0] / 255 * 60

            else:
                raise ValueError("value 0 is not found in green area: {}.".format(color))

        elif color[2] == 255:
            if color[1] == 0:
                # blue to magenta, 240 to 300.
                h = 240 + color[0] / 255 * 60

            elif color[0] == 0:
                # cyan to blue.
                h = 240 - color[1] / 255 * 60

            else:
                raise ValueError("value 0 is not found in blue area: {}.".format(color))

        else:
            raise ValueError("value 255 is not found in color: {}.".format(color))

        return cls.fmt_hsv((h, s, v))

    @classmethod
    def hsv2rgb(cls, hsv):
        """
        Translate hsv color into rgb color.

        Args:
            hsv (tuple or list): hsv color.

        Returns:
            rgb color.
        """

        h, s, v = cls.fmt_hsv(hsv)

        # red to yellow.
        if 0 <= h < 60:
            g = round((h - 0) / 60 * 255)
            color = np.array((255, g, 0))

        # yellow to green.
        elif 60 <= h < 120:
            r = round((1 - (h - 60) / 60) * 255)
            color = np.array((r, 255, 0))

        # green to cyan.
        elif 120 <= h < 180:
            b = round((h - 120) / 60 * 255)
            color = np.array((0, 255, b))

        # cyan to blue.
        elif 180 <= h < 240:
            g = round((1 - (h - 180) / 60) * 255)
            color = np.array((0, g, 255))

        # blue to magenta.
        elif 240 <= h < 300:
            r = round((h - 240) / 60 * 255)
            color = np.array((r, 0, 255))

        # magenta to red.
        elif 300 <= h < 360:
            b = round((1 - (h - 300) / 60) * 255)
            color = np.array((255, 0, b))

        else:
            raise ValueError("unexpect h: {}.".format(h))

        color = color + (color * -1 + 255) * (1 - s)
        color = color * v

        return cls.fmt_rgb(color)

    @classmethod
    def rgb2hec(cls, rgb):
        """
        Translate rgb color into hex code (hec) color.

        Args:
            rgb (tuple or list): rgb color.

        Returns:
            hex code (hec) color.
        """

        r, g, b = cls.fmt_rgb(rgb)

        hec_r = hex(r)[2:].upper()
        hec_g = hex(g)[2:].upper()
        hec_b = hex(b)[2:].upper()

        hec_r = "0" + hec_r if len(hec_r) < 2 else hec_r
        hec_g = "0" + hec_g if len(hec_g) < 2 else hec_g
        hec_b = "0" + hec_b if len(hec_b) < 2 else hec_b

        return cls.fmt_hec(hec_r + hec_g + hec_b)

    @classmethod
    def hec2rgb(cls, hec):
        """
        Translate hex code (hec) color into rgb color.

        Args:
            hec (str): hex code (hec) color.

        Returns:
            rgb color.
        """

        pr_hec_code = cls.fmt_hec(hec)

        hec_r = pr_hec_code[0:2]
        hec_g = pr_hec_code[2:4]
        hec_b = pr_hec_code[4:6]

        r = int("0x{}".format(hec_r), 16)
        g = int("0x{}".format(hec_g), 16)
        b = int("0x{}".format(hec_b), 16)

        return cls.fmt_rgb((r, g, b))

    @classmethod
    def hsv2hec(cls, hsv):
        """
        Translate hsv color into hex code (hec) color.

        Args:
            hsv (tuple or list): hsv color.

        Returns:
            hex code (hec) color.
        """

        rgb = cls.hsv2rgb(hsv)
        hec = cls.rgb2hec(rgb)
        return hec

    @classmethod
    def hec2hsv(cls, hec):
        """
        Translate hex code (hec) color into rgb color.

        Args:
            hec (str): hex code (hec) color.

        Returns:
            rgb color.
        """

        rgb = cls.hec2rgb(hec)
        hsv = cls.rgb2hsv(rgb)
        return hsv


class TestColor(unittest.TestCase):
    def test_translate(self):
        pr_color = Color((0, 0, 0), tp="rgb")

        for r in range(256):
            for g in range(256):
                print("testing rgb2hsv with r, g = {}, {}.".format(r, g))

                for b in range(256):
                    color = Color((r, g, b), tp="rgb")
                    self.assertEqual(color.rgb, (r, g, b))
                    self.assertEqual(color.r, r)
                    self.assertEqual(color.g, g)
                    self.assertEqual(color.b, b)

                    hsv = Color.rgb2hsv(color.rgb)
                    self.assertEqual(color.hsv, tuple(hsv))
                    self.assertEqual(color.h, hsv[0])
                    self.assertEqual(color.s, hsv[1])
                    self.assertEqual(color.v, hsv[2])

                    rgb = Color.hsv2rgb(hsv)
                    self.assertTrue(color.rgb == tuple(rgb))

                    pr_color.r = r
                    pr_color.g = g
                    pr_color.b = b
                    self.assertEqual(pr_color, color)

                    pr_color.h = hsv[0]
                    pr_color.s = hsv[1]
                    pr_color.v = hsv[2]
                    self.assertEqual(pr_color, color)

        for h in range(361):
            for s in range(101):
                print("testing hsv2rgb with r, g = {}, {}.".format(h, s))

                for v in range(101):
                    hsv = np.array([h, s / 100, v / 100])
                    color = Color(hsv, tp="hsv")

                    rgb = Color.hsv2rgb(hsv)
                    ar_hsv = Color.rgb2hsv(rgb)
                    ar_rgb = Color.hsv2rgb(ar_hsv)
                    self.assertTrue((rgb == ar_rgb).all())

                    ar_color = Color(ar_rgb, tp="rgb")
                    self.assertEqual(color, ar_color)

if __name__ == "__main__":
    unittest.main()
