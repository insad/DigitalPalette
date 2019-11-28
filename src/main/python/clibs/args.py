# -*- coding: utf-8 -*-

import os
import json
import re
import time
from clibs.color_set import ColorSet


class Args(object):
    """
    Args object. Manage setting args.
    """

    def __init__(self, resources):
        """
        Init Args object.
        """

        # global args.
        self.global_hm_rules = (
            "analogous",
            "monochromatic",
            "triad",
            "tetrad",
            "pentad",
            "complementary",
            "shades",
            "custom",
        )

        self.global_overflows = (
            "cutoff",
            "return",
            "repeat",
        )

        # load languages.
        all_langs = (
            "en", "ar", "be", "bg", "ca", "cs", "da", "de", "el", "es", 
            "et", "fi", "fr", "hr", "hu", "is", "it", "iw", "ja", "ko", 
            "lt", "lv", "mk", "nl", "no", "pl", "pt", "ro", "ru", "sh", 
            "sk", "sl", "sq", "sr", "sv", "th", "tr", "uk", "zh",
        )

        lang_paths = [(39, "default"),]

        langs_dir = os.sep.join((resources, "langs"))
        if not os.path.isdir(langs_dir):
            os.makedirs(langs_dir)

        for lang in os.listdir(langs_dir):
            if os.path.isfile(os.sep.join((langs_dir, lang))) and lang.split(".")[-1] == "qm":
                glang = re.split("\.|_|-", lang)[0]

                if glang in all_langs:
                    lang_paths.append((all_langs.index(glang), lang))

        self.lang = "default"
        self.usr_langs = tuple(lang_paths)

        # init settings.
        self.usr_store = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette"))
        self.resources = resources

        self.init_settings()

        # load settings.
        if self.store_loc:
            self.load_settings(os.sep.join((self.resources, "settings.json")))

        else:
            self.load_settings(os.sep.join((self.usr_store, "settings.json")))

        # software informations.
        self.info_version = "v2.0.3-dev"
        self.info_main_site = "https://liujiacode.github.io/DigitalPalette"
        self.info_update_site = "https://github.com/liujiacode/DigitalPalette/releases"
        self.info_date = "2019.11.26"
        self.info_author = "Liu Jia"

        # special system settings.
        self.sys_activated_idx = 0
        self.sys_color_set = ColorSet(self.h_range, self.s_range, self.v_range, overflow=self.overflow)
        self.sys_color_set.create(self.hm_rule)

        self.sys_category = 0
        self.sys_channel = 0

    # ---------- ---------- ---------- Public Funcs ---------- ---------- ---------- #

    def init_settings(self):
        """
        Init default settings.
        """

        # load default language.
        self.modify_settings("lang", "en.qm")

        # load local store tag.
        self.store_loc = False

        if os.path.isfile(os.sep.join((self.resources, "settings.json"))):
            try:
                with open(os.sep.join((self.resources, "settings.json")), "r") as sf:
                    uss = json.load(sf)

                    if isinstance(uss, dict) and "store_loc" in uss:
                        self.store_loc = bool(uss["store_loc"])

            except:
                pass

        # need verify and mkdirs.
        if self.store_loc:
            self.usr_color = os.sep.join((self.resources, "MyColors"))
            self.usr_image = os.sep.join((self.resources, "samples"))

        else:
            self.usr_color = os.sep.join((os.path.expanduser('~'), "Documents", "DigitalPalette", "MyColors"))
            self.usr_image = os.sep.join((os.path.expanduser('~'), "Pictures"))

        if not os.path.isdir(self.usr_color):
            os.makedirs(self.usr_color)

        if not os.path.isdir(self.usr_image):
            os.makedirs(self.usr_image)

        self.hm_rule = "analogous"
        self.overflow = "return"
        self.press_move = True
        self.show_hsv = True
        self.show_rgb = True

        self.h_range = (0.0, 360.0)
        self.s_range = (0.68, 1.0)
        self.v_range = (0.68, 1.0)

        self.wheel_ratio = 0.8
        self.volum_ratio = 0.8
        self.cubic_ratio = 0.9

        self.s_tag_radius = 0.08
        self.v_tag_radius = 0.08

        self.zoom_step = 1.1
        self.move_step = 5

        self.circle_dist = 10

        self.positive_wid = 3
        self.negative_wid = 2
        self.wheel_ed_wid = 5

        self.positive_color = (0,   0,   0  )
        self.negative_color = (200, 200, 200)
        self.wheel_ed_color = (230, 230, 230)

    def save_settings(self):
        """
        Save settings to file.
        """

        settings = {
            "version": self.info_version,
            "site": self.info_main_site,
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        }

        items = (
            "usr_color", "usr_image", "store_loc", "hm_rule", "overflow", "lang", "press_move",
            "show_hsv", "show_rgb", "h_range", "s_range", "v_range",
            "wheel_ratio", "volum_ratio", "cubic_ratio",
            "s_tag_radius", "v_tag_radius", "zoom_step", "move_step", "circle_dist",
            "positive_wid", "negative_wid", "wheel_ed_wid",
            "positive_color", "negative_color", "wheel_ed_color",
        )

        for item in items:
            value = getattr(self, item)
            if isinstance(value, (tuple, list)):
                settings[item] = list(value)

            else:
                settings[item] = value

        else:
            if self.store_loc:
                with open(os.sep.join((self.resources, "settings.json")), "w") as sf:
                    json.dump(settings, sf, indent=4)

            else:
                with open(os.sep.join((self.usr_store, "settings.json")), "w") as sf:
                    json.dump(settings, sf, indent=4)

                with open(os.sep.join((self.resources, "settings.json")), "w") as sf:
                    json.dump({"store_loc": False}, sf, indent=4)

    def modify_settings(self, item, value):
        items = {
            "usr_color": lambda vl: self.parse_path(vl),
            "usr_image": lambda vl: self.parse_path(vl),
            "store_loc": lambda vl: self.parse_value(vl, bool),
            "hm_rule": lambda vl: self.parse_selection(vl, self.global_hm_rules, str),
            "overflow": lambda vl: self.parse_selection(vl, self.global_overflows, str),
            "lang": lambda vl: self.parse_selection(vl, [x[1] for x in self.usr_langs], str),
            "press_move": lambda vl: self.parse_value(vl, bool),
            "show_hsv": lambda vl: self.parse_value(vl, bool),
            "show_rgb": lambda vl: self.parse_value(vl, bool),
            "h_range": lambda vl: self.parse_range(vl, (0.0, 360.0), (float, int)),
            "s_range": lambda vl: self.parse_range(vl, (0.0, 1.0), (float, int)),
            "v_range": lambda vl: self.parse_range(vl, (0.0, 1.0), (float, int)),
            "wheel_ratio": lambda vl: self.parse_num(vl, (0.0, 1.0), (float, int)),
            "volum_ratio": lambda vl: self.parse_num(vl, (0.0, 1.0), (float, int)),
            "cubic_ratio": lambda vl: self.parse_num(vl, (0.0, 1.0), (float, int)),
            "s_tag_radius": lambda vl: self.parse_num(vl, (0.0, 0.2), (float, int)),
            "v_tag_radius": lambda vl: self.parse_num(vl, (0.0, 0.2), (float, int)),
            "zoom_step": lambda vl: self.parse_num(vl, (1.0, 10.0), (float, int)),
            "move_step": lambda vl: self.parse_num(vl, (1, 100), (int, float)),
            "circle_dist": lambda vl: self.parse_num(vl, (0, 50), (int, float)),
            "positive_wid": lambda vl: self.parse_num(vl, (0, 20), (int, float)),
            "negative_wid": lambda vl: self.parse_num(vl, (0, 20), (int, float)),
            "wheel_ed_wid": lambda vl: self.parse_num(vl, (0, 20), (int, float)),
            "positive_color": lambda vl: self.parse_color(vl),
            "negative_color": lambda vl: self.parse_color(vl),
            "wheel_ed_color": lambda vl: self.parse_color(vl),
        }

        if item in items:
            ans = items[item](value)

            if ans != "parseerr":
                setattr(self, item, ans)

    def load_settings(self, settings_file):
        """
        Modify default settings by user settings.

        Parameters:
          uss - dict. user settings.
        """

        uss = {}
        if os.path.isfile(settings_file):
            try:
                with open(settings_file, "r") as sf:
                    uss = json.load(sf)

            except:
                pass

        if isinstance(uss, dict):
            if "version" in uss:
                if not self.check_version(uss["version"]):
                    uss = {}

            else:
                uss = {}

        else:
            uss = {}

        for item in uss:
            self.modify_settings(item, uss[item])

    # ---------- ---------- ---------- Classmethods ---------- ---------- ---------- #

    @classmethod
    def parse_path(cls, value):
        """
        Parse value in designed range.
        """

        if isinstance(value, str) and os.path.isdir(value):
            return value

        return "parseerr"

    @classmethod
    def parse_range(cls, value, scope, target_dtype):
        """
        Parse value in designed range.
        """

        if isinstance(value, (tuple, list)) and len(value) == 2 and isinstance(value[0], target_dtype) and isinstance(value[1], target_dtype):
            if scope[0] <= value[0] <= scope[1] and scope[0] <= value[1] <= scope[1]:
                if value[0] <= value[1]:
                    if isinstance(target_dtype, (tuple, list)):
                        return (target_dtype[0](value[0]), target_dtype[0](value[1]))

                    else:
                        return (target_dtype(value[0]), target_dtype(value[1]))

        return "parseerr"

    @classmethod
    def parse_selection(cls, value, selection_list, target_dtype):
        """
        Parse value in designed selection.
        """

        if isinstance(value, target_dtype) and value in selection_list:
            if isinstance(target_dtype, (tuple, list)):
                return target_dtype[0](value)

            else:
                return target_dtype(value)

        return "parseerr"

    @classmethod
    def parse_num(cls, value, scope, target_dtype):
        """
        Parse value in designed scope.
        """

        if isinstance(value, target_dtype) and scope[0] <= value <= scope[1]:
            if isinstance(target_dtype, (tuple, list)):
                return target_dtype[0](value)

            else:
                return target_dtype(value)

        return "parseerr"

    @classmethod
    def parse_value(cls, value, target_dtype):
        """
        Parse value in designed dtype.
        """

        if isinstance(value, target_dtype):
            if isinstance(target_dtype, (tuple, list)):
                return target_dtype[0](value)

            else:
                return target_dtype(value)

        return "parseerr"

    @classmethod
    def parse_color(cls, value):
        """
        Parse value in designed color.
        """

        if isinstance(value, (tuple, list)) and len(value) == 3 and isinstance(value[0], int) and isinstance(value[1], int) and isinstance(value[2], int):
            if 0 <= value[0] <= 255 and 0 <= value[2] <= 255 and 0 <= value[2] <= 255:
                return tuple(value)

        return "parseerr"

    @classmethod
    def check_version(cls, version):
        """
        Check if version is compatible.
        """

        ans = False

        for vre in (r"^v2\.[0].*", r"^v1\.[0].*", ):
            if re.match(vre, version):
                a = re.match(vre, version)
                ans = True
                break

        return ans
