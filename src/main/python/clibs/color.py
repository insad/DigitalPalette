# -*- coding: utf-8 -*-

import numpy as np


class Color(object):
    """
    Color object. The color in object is stored in RGB and HSV type. Default init as black (0, 0, 0).
    """

    def __init__(self, color=(0, 0, 0), ctp="rgb"):
        """
        Init color object from RGB color or Color object.

        Parameters:
          color - numpy.ndarray or Color object. color (R, G, B), and R, G, B in range 0 ~ 255 (int).
          ctp - string. rgb or hsv or hex. indicate the type of input color.
        """

        if isinstance(color, Color):
            self._rgb = color.rgb
            self._hsv = color.hsv
        else:
            if ctp in ("rgb", "hsv", "hex"):
                self.setti(ctp, color)
            else:
                raise ValueError("unknown color type for init: {}.".format(ctp))

    def __repr__(self):
        return "RGB{}".format(self._rgb)

    def __str__(self):
        return "RGB{}".format(self._rgb)

    def getti(self, tag):
        if tag in ("r", "g", "b"):
            values = {"r": self._rgb[0],
                      "g": self._rgb[1],
                      "b": self._rgb[2],}
            return values[tag]

        elif tag in ("h", "s", "v"):
            values = {"h": self._hsv[0],
                      "s": self._hsv[1],
                      "v": self._hsv[2],}
            return values[tag]

        elif tag == "rgb":
            return self._rgb
        elif tag == "hsv":
            return self._hsv
        elif tag == "hex":
            return self.rgb_to_hex(self._rgb)
        else:
            raise ValueError("unexpect tag for gettti: {}.".format(tag))

    def setti(self, tag, value):
        if tag in ("r", "g", "b"):
            optios = {"r": self.setti_r,
                      "g": self.setti_g,
                      "b": self.setti_b,}
            optios[tag](value)

        elif tag in ("h", "s", "v"):
            optios = {"h": self.setti_h,
                      "s": self.setti_s,
                      "v": self.setti_v,}
            optios[tag](value)

        elif tag == "rgb":
            self.setti_rgb(value)
        elif tag == "hsv":
            self.setti_hsv(value)
        elif tag == "hex":
            self.setti_hex_code(value)
        else:
            raise ValueError("unexpect tag for settti: {}.".format(tag))

    @property
    def rgb(self):
        """
        Get RGB color in store.
        """

        return self._rgb

    @rgb.setter
    def rgb(self, rgb):
        self.setti_rgb(rgb)

    def setti_rgb(self, rgb):
        """
        Set RGB color.

        Parameters:
          rgb - numpy.ndarray. color (R, G, B), and R, G, B in range 0 ~ 255 (int).
        """

        self._rgb = self.fmt_rgb(rgb)
        self._hsv = self.rgb_to_hsv(self._rgb)

    @property
    def r(self):
        """
        Get R (first) part of RGB color.
        """

        return self._rgb[0]

    @r.setter
    def r(self, r):
        self.setti_r(r)

    def setti_r(self, r):
        """
        Set R part value.

        Parameters:
          r - int. in range 0 ~ 255.
        """

        rgb = self._rgb.tolist()
        rgb[0] = r
        self._rgb = self.fmt_rgb(rgb)
        self._hsv = self.rgb_to_hsv(self._rgb)

    @property
    def g(self):
        """
        Get G (second) part of RGB color.
        """

        return self._rgb[1]

    @g.setter
    def g(self, g):
        self.setti_g(g)

    def setti_g(self, g):
        """
        Set G part value.

        Parameters:
          g - int. in range 0 ~ 255.
        """

        rgb = self._rgb.tolist()
        rgb[1] = g
        self._rgb = self.fmt_rgb(rgb)
        self._hsv = self.rgb_to_hsv(self._rgb)

    @property
    def b(self):
        """
        Get B (third) part of RGB color.
        """

        return self._rgb[2]

    @b.setter
    def b(self, b):
        self.setti_b(b)

    def setti_b(self, b):
        """
        Set B part value.

        Parameters:
          b - int. in range 0 ~ 255.
        """

        rgb = self._rgb.tolist()
        rgb[2] = b
        self._rgb = self.fmt_rgb(rgb)
        self._hsv = self.rgb_to_hsv(self._rgb)

    @property
    def hsv(self):
        """
        Get HSV color in store.
        """

        return self._hsv

    @hsv.setter
    def hsv(self, hsv):
        self.setti_hsv(hsv)

    def setti_hsv(self, hsv):
        """
        Set HSV color.

        Parameters:
          hsv - numpy.ndarray. color (H, S, V), and H in range 0.0 ~ 360.0, S, V in range 0.0 ~ 1.0 (float).
        """

        self._hsv = self.fmt_hsv(hsv)
        self._rgb = self.hsv_to_rgb(self._hsv)

    @property
    def h(self):
        """
        Get H (first) part of HSV color.
        """

        return self._hsv[0]

    @h.setter
    def h(self, h):
        self.setti_h(h)

    def setti_h(self, h):
        """
        Set H part value.

        Parameters:
          h - float. in range 0.0 ~ 360.0.
        """

        hsv = self._hsv.tolist()
        hsv[0] = h
        self._hsv = self.fmt_hsv(hsv)
        self._rgb = self.hsv_to_rgb(self._hsv)

    @property
    def s(self):
        """
        Get S (second) part of HSV color.
        """

        return self._hsv[1]

    @s.setter
    def s(self, s):
        self.setti_s(s)

    def setti_s(self, s):
        """
        Set S part value.

        Parameters:
          s - float. in range 0.0 ~ 1.0.
        """

        hsv = self._hsv.tolist()
        hsv[1] = s
        self._hsv = self.fmt_hsv(hsv)
        self._rgb = self.hsv_to_rgb(self._hsv)

    @property
    def v(self):
        """
        Get V (third) part of HSV color.
        """

        return self._hsv[2]

    @v.setter
    def v(self, v):
        self.setti_v(v)

    def setti_v(self, v):
        """
        Set V part value.

        Parameters:
          v - float. in range 0.0 ~ 1.0.
        """

        hsv = self._hsv.tolist()
        hsv[2] = v
        self._hsv = self.fmt_hsv(hsv)
        self._rgb = self.hsv_to_rgb(self._hsv)

    @property
    def hex_code(self):
        """
        Get hex code.
        """

        return self.rgb_to_hex(self._rgb)

    @hex_code.setter
    def hex_code(self, hex_code):
        self.setti_hex_code(hex_code)

    def setti_hex_code(self, hex_code):
        """
        Set hex code.

        Parameters:
          hex - string. hex code.
        """

        rgb = self.hex_to_rgb(hex_code)
        self.setti_rgb(rgb)

    @property
    def image(self):
        """
        Get dict type image of color in store.

        Returns:
          dict. {"rgb": rgb_color, "hsv": hsv_color}.
        """

        return {"rgb": self._rgb, "hsv": self._hsv}

    def export(self):
        """
        Get json type image of color in store.

        Returns:
          dict. {"rgb": rgb_color_list, "hsv": hsv_color_list, "hex": hex_code}.
        """

        return {"rgb": self._rgb.tolist(), "hsv": self._hsv.tolist(), "hex": self.rgb_to_hex(self._rgb)}

    def overflow_s(self, s):
        """
        Set S part value with overflow prevented.

        Parameters:
          s - float.
        """

        if float(s) // 1.0 % 2.0 == 0.0:
            pr_s = s % 1.0
        else:
            pr_s = 1 - (s % 1)

        self.setti_s(pr_s)

    def overflow_v(self, v):
        """
        Set V part value with overflow prevented.

        Parameters:
          v - float.
        """

        if float(v) // 1.0 % 2.0 == 0.0:
            pr_v = v % 1.0
        else:
            pr_v = 1 - (v % 1)

        self.setti_v(pr_v)

    @classmethod
    def fmt_rgb(cls, rgb):
        """
        Class method. Verify and format RGB color to standard type.

        Parameters:
          rgb - numpy.ndarray. color (R, G, B), and R, G, B in range 0 ~ 255 (int).

        Returns:
          numpy.ndarray. color (R, G, B).
        """

        if len(rgb) == 3:
            _rgb = np.rint(rgb)

            if (_rgb >= (0, 0, 0)).all() and (_rgb <= (255, 255, 255)).all():
                return _rgb.astype(np.uint8)
            else:
                raise ValueError("expect R, G, B in range 0 ~ 255: {}.".format(rgb))

        else:
            raise ValueError("expect RGB color length 3: {}.".format(rgb))

    @classmethod
    def fmt_hsv(cls, hsv):
        """
        Class method. Verify and format HSV color to standard type.

        Parameters:
          hsv - numpy.ndarray. color (H, S, V), and H in range 0.0 ~ 360.0, S, V in range 0.0 ~ 1.0 (float).

        Returns:
          numpy.ndarray. color (H, S, V).
        """

        if len(hsv) == 3:
            _h, _s, _v = hsv
            _h = round(_h % 360.0 * 1E5) / 1E5
            _s = round(_s * 1E5) / 1E5
            _v = round(_v * 1E5) / 1E5

            if not (0.0 <= _s <= 1.0 and 0.0 <= _v <= 1.0):
                raise ValueError("expect S, V in range 0.0~1.0: {}.".format(hsv))

            return np.array((_h, _s, _v), dtype=np.float32)

        else:
            raise ValueError("expect HSV color length 3: {}.".format(hsv))

    @classmethod
    def fmt_hex(cls, hex_code):
        """
        Class method. Verify and format hex code to standard type.

        Parameters:
          hex_code - string. hex code.

        Returns:
          string. hex code.
        """

        if isinstance(hex_code, str):
            if len(hex_code) == 6:
                for stri in hex_code:
                    if stri not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"):
                        raise ValueError("expect code in hex type: {}.".format(hex_code))
            else:
                raise ValueError("expect hex code length 6: {}.".format(hex_code))
        else:
            raise ValueError("expect hex code in string type: {}.".format(hex_code))

        return hex_code

    @classmethod
    def rgb_to_hsv(cls, rgb):
        """
        Class method. Translating RGB type color to HSV type.

        Parameters:
          rgb - numpy.ndarray. color (R, G, B), and R, G, B in range 0 ~ 255 (int).

        Returns:
          numpy.ndarray. color (H, S, V).
        """

        color = cls.fmt_rgb(rgb)

        v = max(color) / 255.0
        if abs(v - 0) < 1E-5:
            color = np.array((255, 0, 0))
            # return 0, 1, 0
        else:
            color = color / v

        s = 1 - min(color) / 255.0
        if abs(s - 0) < 1E-5:
            color = np.array((255, 0, 0))
            # return 0, 0, 1
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
    def hsv_to_rgb(cls, hsv):
        """
        Class method. Translating HSV type color to RGB type.

        Parameters:
          hsv - numpy.ndarray. color (H, S, V), and H in range 0.0 ~ 360.0, S, V in range 0.0 ~ 1.0 (float).

        Returns:
          numpy.ndarray. color (R, G, B).
        """

        H, S, V = cls.fmt_hsv(hsv)

        # red to yellow.
        if 0 <= H < 60:
            g = round((H - 0) / 60 * 255)
            color = np.array((255, g, 0))
        # yellow to green.
        elif 60 <= H < 120:
            r = round((1 - (H - 60) / 60) * 255)
            color = np.array((r, 255, 0))
        # green to cyan.
        elif 120 <= H < 180:
            b = round((H - 120) / 60 * 255)
            color = np.array((0, 255, b))
        # cyan to blue.
        elif 180 <= H < 240:
            g = round((1 - (H - 180) / 60) * 255)
            color = np.array((0, g, 255))
        # blue to magenta.
        elif 240 <= H < 300:
            r = round((H - 240) / 60 * 255)
            color = np.array((r, 0, 255))
        # magenta to red.
        elif 300 <= H < 360:
            b = round((1 - (H - 300) / 60) * 255)
            color = np.array((255, 0, b))
        else:
            raise ValueError("unexpect H: {}.".format(H))

        color = color + (color * -1 + 255) * (1 - S)
        color = color * V
        color = np.rint(color).astype(int)

        return cls.fmt_rgb(color)

    @classmethod
    def rgb_to_hex(cls, rgb):
        """
        Class method. Translating RGB type color to hex code.

        Parameters:
          rgb - numpy.ndarray. color (R, G, B), and R, G, B in range 0 ~ 255 (int).

        Returns:
          sting. hex code.
        """

        r, g, b = cls.fmt_rgb(rgb)

        hex_r = hex(r)[2:].upper()
        hex_g = hex(g)[2:].upper()
        hex_b = hex(b)[2:].upper()

        hex_r = "0" + hex_r if len(hex_r) < 2 else hex_r
        hex_g = "0" + hex_g if len(hex_g) < 2 else hex_g
        hex_b = "0" + hex_b if len(hex_b) < 2 else hex_b

        return cls.fmt_hex(hex_r + hex_g + hex_b)

    @classmethod
    def hex_to_rgb(cls, hex_code):
        """
        Class method. Translating hex code to RGB type color.

        Parameters:
          hex_code - string. hex code.

        Returns:
          numpy.ndarray. color (R, G, B).
        """

        pr_hex_code = cls.fmt_hex(hex_code)

        hex_r = pr_hex_code[0:2]
        hex_g = pr_hex_code[2:4]
        hex_b = pr_hex_code[4:6]

        r = int("0x{}".format(hex_r), 16)
        g = int("0x{}".format(hex_g), 16)
        b = int("0x{}".format(hex_b), 16)

        return cls.fmt_rgb((r, g, b))
    
    def hsv_eq(self, hsv, acr=1E-5):
        if (np.abs(self._hsv - np.array(hsv)) < acr).all():
            return True
        else:
            return False
    
    def rgb_eq(self, rgb):
        if (self._rgb == np.array(rgb)).all():
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.rgb_eq(other.rgb)
        else:
            raise ValueError("expect the other color in Color object.")

    def __ne__(self, other):
        if self.__eq__(other):
            return False
        else:
            return True


if __name__ == "__main__":
    for r in range(256):
        print(r)
        for g in range(256):
            for b in range(256):
                rgb = np.array([r, g, b])
                hsv = Color.rgb_to_hsv(rgb)
                _rgb = Color.hsv_to_rgb(hsv)
                _hsv = Color.rgb_to_hsv(_rgb)
                
                if not (hsv == _hsv).all():
                    raise ValueError("{}, {}, {}, {}".format(hsv, rgb, _hsv, _rgb))

    for h in range(361):
        print(h)
        for s in range(101):
            for v in range(101):
                hsv = np.array([h, s / 100, v / 100])
                rgb = Color.hsv_to_rgb(hsv)
                _hsv = Color.rgb_to_hsv(rgb)
                _rgb = Color.hsv_to_rgb(_hsv)

                if not (rgb == _rgb).all():
                    raise ValueError("{}, {}, {}, {}".format(rgb, hsv, _rgb, _hsv))
    