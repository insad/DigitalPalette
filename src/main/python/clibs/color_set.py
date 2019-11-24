# -*- coding: utf-8 -*-

import random
import binascii
from clibs.color import Color


class ColorSet(object):
    """
    ColorSet object. Storing five colors in in different harmony rules (analogous, monochromatic,triad, tetrad, pentad,
    complementary, shades and custom) and sequence 2, 1, 0, 3, 4.
    """

    def __init__(self, h_range, s_range, v_range, overflow="cutoff"):
        """
        Init ColorSet object.

        Args:
            h_range (tuple or list): the initial range of h value. such as (0.0, 360.0).
            s_range (tuple or list): the initial range of s value. such as (0.8, 1.0).
            v_range (tuple or list): the initial range of v value. such as (0.8, 1.0).
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        self.set_hsv_ranges(h_range, s_range, v_range)

        assert 0.0 <= self._h_range[0] <= 360.0
        assert 0.0 <= self._h_range[1] <= 360.0
        assert self._h_range[0] <= self._h_range[1]

        assert 0.0 <= self._s_range[0] <= 1.0
        assert 0.0 <= self._s_range[1] <= 1.0
        assert self._s_range[0] <= self._s_range[1]

        assert 0.0 <= self._v_range[0] <= 1.0
        assert 0.0 <= self._v_range[1] <= 1.0
        assert self._v_range[0] <= self._v_range[1]

        self._color_set = [
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            Color((0, 0, 0), tp="rgb", overflow=overflow),
            ]

        self._custom_create()

    # ---------- ---------- ---------- Setting and Getting Funcs ---------- ---------- ---------- #

    def set_hsv_ranges(self, h_range, s_range, v_range):
        """
        Set the h, s, v ranges for creating color set.
        """

        if isinstance(h_range, (tuple, list)) and isinstance(s_range, (tuple, list)) and isinstance(v_range, (tuple, list)):
            self._h_range = tuple([float(i) for i in h_range[:2]])
            self._s_range = tuple([float(i) for i in s_range[:2]])
            self._v_range = tuple([float(i) for i in v_range[:2]])

        else:
            raise ValueError("expect h, s, v ranges in tuple or list type: {}, {}, {}.".format(h_range, s_range, v_range))

    def set_overflow(self, overflow):
        """
        Set the overflow method for each color in color set.

        Args:
            overflow (str): method to manipulate overflowed s and v values, in "cutoff", "return" and "repeat".
        """

        for color in self._color_set:
            color.set_overflow(overflow)

    def get_overflow(self):
        """
        Get the overflow method of first color in color set.
        """

        assert self._color_set[1].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[2].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[3].get_overflow() == self._color_set[0].get_overflow()
        assert self._color_set[4].get_overflow() == self._color_set[0].get_overflow()

        return self._color_set[0].get_overflow()

    # ---------- ---------- ---------- Inner Funcs ---------- ---------- ---------- #

    def __str__(self):
        """
        Str format.
        """

        return "ColorSet({}, {}, {}, {}, {})".format(*self._color_set)

    def __repr__(self):
        """
        Repr format.
        """

        return "ColorSet({}, {}, {}, {}, {})".format(*self._color_set)

    def __getitem__(self, idx):
        """
        Get color item in color set.
        """

        return self._color_set[idx]

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def backup(self):
        """
        Backup the color set as a tuple.
        """

        color_set = (
            Color(self._color_set[0], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[1], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[2], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[3], tp="color", overflow=self.get_overflow()),
            Color(self._color_set[4], tp="color", overflow=self.get_overflow()),
        )
        return color_set

    def recover(self, color_set):
        """
        Recover the color set by a tuple.
        """

        self._color_set = list(color_set)

    def create(self, harmony_rule):
        """
        Create color set under a selected harmony rule.

        Args:
            harmony_rule (str): rule, in "analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades" and "custom".
        """

        methods = {
            "analogous": self._analogous_create,
            "monochromatic": self._monochromatic_create,
            "triad": self._triad_create,
            "tetrad": self._tetrad_create,
            "pentad": self._pentad_create,
            "complementary": self._complementary_create,
            "shades": self._shades_create,
            "custom": self._custom_create,
        }

        if harmony_rule in methods:
            methods[harmony_rule]()

        else:
            raise ValueError("expect harmony rule in list 'analogous', 'monochromatic', etc.: {}.".format(harmony_rule))

    def modify(self, harmony_rule, idx, color):
        """
        Modify color set under a selected harmony rule.

        Args:
            harmony_rule (str): rule, in "analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades" and "custom".
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        methods = {
            "analogous": self._analogous_modify,
            "monochromatic": self._single_modify,
            "triad": self._multiple_modify,
            "tetrad": self._tetrad_modify,
            "pentad": self._multiple_modify,
            "complementary": self._multiple_modify,
            "shades": self._single_modify,
            "custom": self._custom_modify,
        }

        if harmony_rule in methods:
            methods[harmony_rule](idx, color)

        else:
            raise ValueError("unexpect harmony rule name for modify: {}.".format(harmony_rule))

    def export_dict(self):
        """
        Export color set in dict type (for json file).

        Returns:
            color set dict {2: color_2, 1: color_1, 0: color_0, 3： color_3, 4: color_4}.
        """

        color_dict = {}
        for i in (2, 1, 0, 3, 4):
            color_dict["color_{}".format(i)] = self._color_set[i].export()

        return color_dict

    def export_swatch(self):
        """
        Export color set in swatch type (for GIMP file).

        Returns:
            Binary strings.
        """

        swatch_chars_v1 = "00010005"
        swatch_chars_v2 = "00020005"

        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), int(s * 65535), int(v * 65535))
            swatch_chars_v1 += pr_chars

            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "0000{:0>4x}".format(11) + "{:0>4x}{:0>4x}{:0>4x}{:0>4x}{:0>4x}{:0>4x}{:0>4x}{:0>4x}{:0>4x}".format(ord("D"), ord("i"), ord("g"), ord("i"), ord("P"), ord("a"), ord("l"), ord("e"), ord("_")) + "{:0>4x}0000".format(ord(str(i)))

        swatch_chars = swatch_chars_v1 + swatch_chars_v2

        return binascii.a2b_hex(swatch_chars)

    def export_text(self):
        """
        Export color set in plain text for directly read.

        Returns:
            Plain text.
        """

        color_text = "{:<12}{:<10}{:<10}{:<10}{:<12}{:<12}{:<12}{:<8}\n".format("# Index", "R", "G", "B", "H", "S", "V", "Hex code")
        for i in (2, 1, 0, 3, 4):
            r, g, b = self._color_set[i].rgb
            h, s, v = self._color_set[i].hsv
            hex_code = "#" + self._color_set[i].hec
            color_text += "  {:<10}{:<10}{:<10}{:<10}{:<12.2f}{:<12.2f}{:<12.2f}{:<8}\n".format(i, r, g, b, h, s, v, hex_code)

        return color_text

    def import_color_set(self, color_set):
        """
        Import color set from list.

        Args:
            color_set (tuple or list): color set list.
        """

        self._color_set = list(color_set)

    # ---------- ---------- ---------- Personal Funcs ---------- ---------- ---------- #

    def _rotate(self, delta_h, delta_s, delta_v):
        """
        Rotate color set by delta values.

        Args:
            delta_h (int or float): shift value for h.
            delta_s (int or float): shift value for s.
            delta_v (int or float): shift value for v.
        """

        for idx in range(5):
            self._color_set[idx].h = self._color_set[idx].h + delta_h
            self._color_set[idx].s = self._color_set[idx].s + delta_s
            self._color_set[idx].v = self._color_set[idx].v + delta_v

    def _analogous_create(self):
        """
        Create color set in analogous rule.
        """

        angle = (self._color_set[3].h - self._color_set[1].h) / 2

        self._color_set[1].h = self._color_set[0].h - angle
        self._color_set[2].h = self._color_set[0].h - angle * 2
        self._color_set[3].h = self._color_set[0].h + angle
        self._color_set[4].h = self._color_set[0].h + angle * 2

    def _analogous_modify(self, idx, pr_color):
        """
        Modify color set in analogous rule.

        Args:
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        if idx == 0:
            delta_h = pr_color.h - self._color_set[0].h
            delta_s = pr_color.s - self._color_set[0].s
            delta_v = pr_color.v - self._color_set[0].v

            self._rotate(delta_h, delta_s, delta_v)

        else:
            if idx in (1, 2):
                angle = self._color_set[0].h - pr_color.h

            elif idx in (3, 4):
                angle = pr_color.h - self._color_set[0].h

            else:
                raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))

            # place the turning point at relative 180 deg.
            if idx in (2, 4):
                angle = angle - 360 if angle > 180 else angle
                angle = angle + 360 if angle < -180 else angle
                angle /= 2

            self._color_set[1].h = self._color_set[0].h - angle
            self._color_set[2].h = self._color_set[0].h - angle * 2
            self._color_set[3].h = self._color_set[0].h + angle
            self._color_set[4].h = self._color_set[0].h + angle * 2

        self._color_set[idx] = pr_color

    def _monochromatic_create(self):
        """
        Create color set in monochromatic rule.
        """

        self._color_set[1].h = self._color_set[0].h
        self._color_set[2].h = self._color_set[0].h
        self._color_set[3].h = self._color_set[0].h
        self._color_set[4].h = self._color_set[0].h

        us_random = self._color_set[0].s
        ls_random = self._color_set[0].s
        if us_random < 0.5:
            us_random += 0.4 * random.random()
            ls_random += 0.1 * random.random()

        else:
            us_random -= 0.4 * random.random()
            ls_random -= 0.1 * random.random()

        uv_random = self._color_set[0].v
        lv_random = self._color_set[0].v
        if uv_random < 0.5:
            uv_random += 0.4 * random.random()
            lv_random += 0.1 * random.random()

        else:
            uv_random -= 0.4 * random.random()
            lv_random -= 0.1 * random.random()

        self._color_set[1].s = us_random
        self._color_set[2].s = us_random
        self._color_set[3].s = ls_random
        self._color_set[4].s = ls_random

        self._color_set[1].v = uv_random
        self._color_set[2].v = lv_random
        self._color_set[3].v = uv_random
        self._color_set[4].v = lv_random

    def _single_modify(self, idx, pr_color):
        """
        Modify color set in single method for monochromatic and shades rules.

        Args:
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        if idx == 0:
            delta_h = pr_color.h - self._color_set[0].h
            delta_s = pr_color.s - self._color_set[0].s
            delta_v = pr_color.v - self._color_set[0].v

            self._rotate(delta_h, delta_s, delta_v)

        else:
            if idx in range(5):
                for i in range(5):
                    self._color_set[i].h = pr_color.h

            else:
                raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))

        self._color_set[idx] = pr_color

    def _triad_create(self):
        """
        Create color set in triad rule.
        """

        self._color_set[1].h = self._color_set[0].h - 120.0
        self._color_set[2].h = self._color_set[0].h - 120.0
        self._color_set[3].h = self._color_set[0].h + 120.0
        self._color_set[4].h = self._color_set[0].h + 120.0

    def _multiple_modify(self, idx, pr_color):
        """
        Modify color set in multiple method for triad, pentad and complementary rules.

        Args:
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        if idx == 0:
            delta_h = pr_color.h - self._color_set[idx].h
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v

            self._rotate(delta_h, delta_s, delta_v)

        else:
            delta_h = pr_color.h - self._color_set[idx].h

            if idx in range(5):
                for i in range(5):
                    self._color_set[i].h += delta_h

            else:
                raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))

        self._color_set[idx] = pr_color

    def _tetrad_create(self):
        """
        Create color set in tetrad rule.
        """

        self._color_set[1].h = self._color_set[0].h
        self._color_set[2].h = self._color_set[0].h - 90
        self._color_set[3].h = self._color_set[0].h + 90
        self._color_set[4].h = self._color_set[0].h + 180

    def _tetrad_modify(self, idx, pr_color):
        """
        Modify color set in tetrad rule.

        Args:
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        if idx == 0:
            delta_h = pr_color.h - self._color_set[idx].h
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v

            self._rotate(delta_h, delta_s, delta_v)

        else:
            delta_h = pr_color.h - self._color_set[idx].h

            if idx in (1, 4):
                self._color_set[0].h += delta_h
                self._color_set[1].h += delta_h
                self._color_set[4].h += delta_h

            elif idx in (2, 3):
                self._color_set[2].h += delta_h
                self._color_set[3].h += delta_h

            else:
                raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))

        self._color_set[idx] = pr_color

    def _pentad_create(self):
        """
        Create color set in pentad rule.
        """

        self._color_set[1].h = self._color_set[0].h - 72
        self._color_set[2].h = self._color_set[0].h - 144
        self._color_set[3].h = self._color_set[0].h + 72
        self._color_set[4].h = self._color_set[0].h + 144

    def _complementary_create(self):
        """
        Create color set in complementary rule.
        """

        self._color_set[1].h = self._color_set[0].h
        self._color_set[2].h = self._color_set[0].h + 180.0
        self._color_set[3].h = self._color_set[0].h
        self._color_set[4].h = self._color_set[0].h + 180.0

        us_random = self._color_set[0].s
        ls_random = self._color_set[0].s
        if us_random < 0.5:
            us_random += 0.4 * random.random()
            ls_random += 0.1 * random.random()

        else:
            us_random -= 0.4 * random.random()
            ls_random -= 0.1 * random.random()

        uv_random = self._color_set[0].v
        lv_random = self._color_set[0].v
        if uv_random < 0.5:
            uv_random += 0.4 * random.random()
            lv_random += 0.1 * random.random()

        else:
            uv_random -= 0.4 * random.random()
            lv_random -= 0.1 * random.random()

        self._color_set[1].s = us_random
        self._color_set[2].s = us_random
        self._color_set[3].s = ls_random
        self._color_set[4].s = ls_random

        self._color_set[1].v = uv_random
        self._color_set[2].v = lv_random
        self._color_set[3].v = uv_random
        self._color_set[4].v = lv_random

    def _shades_create(self):
        """
        Create color set in shades rule.
        """

        self._color_set[1].hsv = self._color_set[0].hsv
        self._color_set[2].hsv = self._color_set[0].hsv
        self._color_set[3].hsv = self._color_set[0].hsv
        self._color_set[4].hsv = self._color_set[0].hsv

        self._color_set[1].v = 0.15
        self._color_set[2].v = 0.40
        self._color_set[3].v = 0.65
        self._color_set[4].v = 0.90

    def _custom_create(self):
        """
        Create color set in custom rule.
        """

        for i in range(5):
            h = self._h_range[0] + (self._h_range[1] - self._h_range[0]) * random.random()
            s = self._s_range[0] + (self._s_range[1] - self._s_range[0]) * random.random()
            v = self._v_range[0] + (self._v_range[1] - self._v_range[0]) * random.random()

            self._color_set[i].hsv = (h, s, v)

    def _custom_modify(self, idx, pr_color):
        """
        Modify color set in custom rule.

        Args:
            idx (int): index in range 0 ~ 4 which indicates the color in color set for modify.
            color (Color): replace the selected color with this color.
        """

        if idx in range(5):
            self._color_set[idx].hsv = pr_color.hsv

        else:
            raise ValueError("expect idx in range 0 ~ 4: {}.".format(idx))
