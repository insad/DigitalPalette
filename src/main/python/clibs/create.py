# -*- coding: utf-8 -*-

from clibs.color import Color
import random
import binascii


class Create(object):
    """
    Create action object. Creating color set with different harmony rules (analogous, monochromatic, triad, 
    tetrad, pentad, complementary, shades and custom).

    Color set sequence in displays: 2, 1, 0, 3, 4.
    """

    def __init__(self, h_range, s_range, v_range):
        """
        Create initial color set with H, S, V ranges.

        Parameters:
          h_range - tuple or list. the initial range of H value. such as (0.0, 360.0).
          s_range - tuple or list. the initial range of S value. such as (0.8, 1.0).
          v_range - tuple or list. the initial range of V value. such as (0.8, 1.0).
        """

        # The range of HSV values. Initial color set would be generated and limited in these ranges.
        if isinstance(h_range, (tuple, list)) and isinstance(s_range, (tuple, list)) and isinstance(v_range, (tuple, list)):
            pr_h_range = tuple([float(i) for i in h_range[:2]])
            pr_s_range = tuple([float(i) for i in s_range[:2]])
            pr_v_range = tuple([float(i) for i in v_range[:2]])
        else:
            raise ValueError("expect h, s, v ranges in tuple or list type: {}, {}, {}.".format(h_range, s_range, v_range))

        # The initial color set contains five random colors.
        self._color_set = []
        for _ in range(5):
            h = pr_h_range[0] + (pr_h_range[1] - pr_h_range[0]) * random.random()
            s = pr_s_range[0] + (pr_s_range[1] - pr_s_range[0]) * random.random()
            v = pr_v_range[0] + (pr_v_range[1] - pr_v_range[0]) * random.random()

            c = Color((h, s, v), ctp="hsv")
            self._color_set.append(c)

    @property
    def color_set(self):
        return self._color_set

    def rotate(self, delta_h, delta_s, delta_v):
        for idx in range(5):
            self._color_set[idx].h += delta_h
            self._color_set[idx].overflow_s(self._color_set[idx].s + delta_s)
            self._color_set[idx].overflow_v(self._color_set[idx].v + delta_v)

    def _analogous_create(self):
        """
        Create color set in analogous rule.
        """

        angle = (self._color_set[0].h - self._color_set[1].h) * 0.3

        self._color_set[1].h = self._color_set[0].h - angle
        self._color_set[2].h = self._color_set[0].h - angle * 2
        self._color_set[3].h = self._color_set[0].h + angle
        self._color_set[4].h = self._color_set[0].h + angle * 2

    def _analogous_modify(self, idx, color):
        """
        Modify color set in analogous rule.
        """

        pr_color = Color(color=color)

        if idx == 0:
            delta_h = pr_color.h - self._color_set[0].h
            delta_s = pr_color.s - self._color_set[0].s
            delta_v = pr_color.v - self._color_set[0].v

            self.rotate(delta_h, delta_s, delta_v)

        elif idx < 5:
            if idx == 1 or idx == 2:
                angle = (self._color_set[0].h - pr_color.h) / idx
            elif idx == 3 or idx == 4:
                angle = (pr_color.h - self._color_set[0].h) / (idx - 2)
            else:
                raise ValueError("unexpect index in analogous modify: {}.".format(idx))

            self._color_set[1].h = self._color_set[0].h - angle
            self._color_set[2].h = self._color_set[0].h - angle * 2
            self._color_set[3].h = self._color_set[0].h + angle
            self._color_set[4].h = self._color_set[0].h + angle * 2

        else:
            raise ValueError("unexpect index in analogous modify: {}.".format(idx))

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
            us_random += 0.5 * random.random()
            ls_random += 0.1 * random.random()
        else:
            us_random -= 0.5 * random.random()
            ls_random -= 0.1 * random.random()

        uv_random = self._color_set[0].v
        lv_random = self._color_set[0].v
        if uv_random < 0.5:
            uv_random += 0.5 * random.random()
            lv_random = 0.1 * random.random()
        else:
            uv_random -= 0.5 * random.random()
            lv_random -= 0.1 * random.random()

        self._color_set[1].s = us_random
        self._color_set[2].s = us_random
        self._color_set[3].s = ls_random
        self._color_set[4].s = ls_random

        self._color_set[1].v = uv_random
        self._color_set[2].v = lv_random
        self._color_set[3].v = uv_random
        self._color_set[4].v = lv_random

    def _single_modify(self, idx, color):
        """
        Modify color set in single method for monochromatic and shades rules.
        """

        pr_color = Color(color=color)

        if idx == 0:
            delta_h = pr_color.h - self._color_set[0].h
            delta_s = pr_color.s - self._color_set[0].s
            delta_v = pr_color.v - self._color_set[0].v

            self.rotate(delta_h, delta_s, delta_v)

        elif idx < 5:
            for i in range(5):
                self._color_set[i].h = pr_color.h

        else:
            raise ValueError("unexpect index in single modify: {}.".format(idx))

        self._color_set[idx] = pr_color

    def _triad_create(self):
        """
        Create color set in triad rule.
        """

        self._color_set[1].h = self._color_set[0].h - 120.0
        self._color_set[2].h = self._color_set[0].h - 120.0
        self._color_set[3].h = self._color_set[0].h + 120.0
        self._color_set[4].h = self._color_set[0].h + 120.0
    
    def _multiple_modify(self, idx, color):
        """
        Modify color set in multiple method for triad, pentad and complementary rules.
        """

        pr_color = Color(color=color)
        delta_h = pr_color.h - self._color_set[idx].h

        if idx == 0:
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
            self.rotate(delta_h, delta_s, delta_v)

        elif idx < 5:
            for i in range(5):
                self._color_set[i].h += delta_h

        else:
            raise ValueError("unexpect index in synchronous modify: {}.".format(idx))

        self._color_set[idx] = pr_color

    def _tetrad_create(self):
        """
        Create color set in tetrad rule.
        """

        self._color_set[1].h = self._color_set[0].h
        self._color_set[2].h = self._color_set[0].h - 90
        self._color_set[3].h = self._color_set[0].h + 90
        self._color_set[4].h = self._color_set[0].h + 180

    def _tetrad_modify(self, idx, color):
        """
        Modify color set in tetrad rule.
        """

        pr_color = Color(color=color)
        delta_h = pr_color.h - self._color_set[idx].h

        if idx == 0:
            delta_s = pr_color.s - self._color_set[idx].s
            delta_v = pr_color.v - self._color_set[idx].v
            self.rotate(delta_h, delta_s, delta_v)

        elif idx < 5:
            if idx == 1 or idx == 4:
                self._color_set[0].h += delta_h
                self._color_set[1].h += delta_h
                self._color_set[4].h += delta_h
            elif idx == 2 or idx == 3:
                self._color_set[2].h += delta_h
                self._color_set[3].h += delta_h
            else:
                raise ValueError("unexpect index in tetrad modify: {}.".format(idx))

        else:
            raise ValueError("unexpect index in tetrad modify: {}.".format(idx))

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
            lv_random = 0.1 * random.random()
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

        self._color_set[1] = Color(self._color_set[0])
        self._color_set[2] = Color(self._color_set[0])
        self._color_set[3] = Color(self._color_set[0])
        self._color_set[4] = Color(self._color_set[0])

        self._color_set[1].v = 0.25
        self._color_set[2].v = 0.5
        self._color_set[3].v = 0.75
        self._color_set[4].v = 1.0

    def _custom_modify(self, idx, color):
        """
        Modify color set in custom rule.
        """
        if idx < 5:
            self._color_set[idx] = Color(color=color)

        else:
            raise ValueError("unexpect index in custom modify: {}.".format(idx))

    def create(self, harmony_rule):
        """
        Create color set in a selected harmony rule.

        Parameters:
          harmony_rule - string. harmony rule like analogous, monochromatic, triad, tetrad, pentad, 
          complementary, shades and custom.
        """

        if harmony_rule == "custom":
            return
        else:
            methods = {"analogous": self._analogous_create,
                       "monochromatic": self._monochromatic_create,
                       "triad": self._triad_create,
                       "tetrad": self._tetrad_create,
                       "pentad": self._pentad_create,
                       "complementary": self._complementary_create,
                       "shades": self._shades_create,
                       }
            
            if harmony_rule in methods:
                methods[harmony_rule]()
            else:
                raise ValueError("unexpect harmony rule name for create: {}.".format(harmony_rule))

    def modify(self, harmony_rule, idx, color):
        """
        Modify color set under a selected harmony rule.

        Parameters:
          harmony_rule - string. harmony rule like analogous, monochromatic, triad, tetrad, pentad, 
          complementary, shades and custom.
          idx - int. index in range 0 ~ 4 which indicates the color in color set for modify.
          color - Color. replace the selected color with this color.
        """

        methods = {"analogous": self._analogous_modify,
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

    def export_color_set(self):
        color_dict = {}
        for i in (2, 1, 0, 3, 4):
            color_dict["color_{}".format(i)] = self._color_set[i].export()

        return color_dict

    def export_swatch(self):
        swatch_chars_v1 = "00010019"
        swatch_chars_v2 = "00020019"

        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), int(s * 65535), int(v * 65535))
            swatch_chars_v1 += pr_chars
            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "00000003" + "{:0>4x}".format(ord("N")) + "{:0>4x}0000".format(ord(str(i)))
        
        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), 65535, 65535)
            swatch_chars_v1 += pr_chars
            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "00000003" + "{:0>4x}".format(ord("F")) + "{:0>4x}0000".format(ord(str(i)))
        
        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), 32768, 65535)
            swatch_chars_v1 += pr_chars
            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "00000003" + "{:0>4x}".format(ord("S")) + "{:0>4x}0000".format(ord(str(i)))
        
        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), 65535, 32768)
            swatch_chars_v1 += pr_chars
            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "00000003" + "{:0>4x}".format(ord("V")) + "{:0>4x}0000".format(ord(str(i)))
        
        for i in (2, 1, 0, 3, 4):
            h, s, v = self._color_set[i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), 32768, 32768)
            swatch_chars_v1 += pr_chars
            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "00000003" + "{:0>4x}".format(ord("H")) + "{:0>4x}0000".format(ord(str(i)))

        swatch_chars = swatch_chars_v1 + swatch_chars_v2

        return binascii.a2b_hex(swatch_chars)

    def import_color_set(self, color_dict):
        color_set = []

        color_cmp = False
        for i in range(5):
            try:
                color_set.append(Color(color_dict["color_{}".format(i)]["hsv"], ctp="hsv"))
                color_cmp = True
            except:
                color_cmp = False
                raise ValueError("Can not import hsv color {}: {}.".format(i, color_dict["color_{}".format(i)]["hsv"]))

        if color_cmp:
            self._color_set = color_set
