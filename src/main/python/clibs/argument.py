# -*- coding: utf-8 -*-

from clibs import info as dpinfo
import os
import json


class Argument(object):
    """
    Argument object. Manage setting args.
    """

    def __init__(self, default_setti, setti_file):
        """
        Load initial settings.
        """

        self._setti = {"version": dpinfo.current_version(),}
        self._setti.update(default_setti)
        self.err = ""

        if os.path.isfile(setti_file):
            with open(setti_file, "r") as sf:
                uss = json.load(sf)

                if "version" in uss:
                    if dpinfo.if_version_compatible(uss["version"]):
                        self.setting(uss)
                    else:
                        self.err = "Version is not compatible: {}. Using default settings instead.".format(uss["version"])

                else:
                    self.err = "Version information is not found in settings.json. Using default settings instead."

    @property
    def settings(self):
        return self._setti
    
    def save_settings(self, setti_file):
        """
        Save settings to file.
        """

        with open(setti_file, "w") as sf:
            json.dump(self._setti, sf, indent=4)

    def setting(self, uss):
        """
        Modify default settings by user settings.

        Parameters:
          uss - dict. user settings.
        """

        if "h_range" in uss:
            self.parse_range("h_range", uss["h_range"], (int, float), (0.0, 360.0), float)
        
        if "s_range" in uss:
            self.parse_range("s_range", uss["s_range"], (int, float), (0.0, 1.0), float)
        
        if "v_range" in uss:
            self.parse_range("v_range", uss["v_range"], (int, float), (0.0, 1.0), float)
        
        if "hm_rule" in uss:
            self.parse_selection("hm_rule", uss["hm_rule"], ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom"))

        if "radius" in uss:
            self.parse_num("radius", uss["radius"], (int, float), (0.0, 1.0), float)
        
        if "color_radius" in uss:
            self.parse_num("color_radius", uss["color_radius"], (int, float), (0.0, 1.0), float)
        
        if "color_radius" in uss:
            self.parse_num("color_radius", uss["color_radius"], (int, float), (0.0, 1.0), float)
        
        if "tip_radius" in uss:
            self.parse_num("tip_radius", uss["tip_radius"], (int, float), (0.0, 1.0), float)
        
        if "widratio" in uss:
            self.parse_num("widratio", uss["widratio"], (int, float), (0.0, 1.0), float)
        
        if "bar_widratio" in uss:
            self.parse_num("bar_widratio", uss["bar_widratio"], (int, float), (0.0, 1.0), float)
        
        if "press_move" in uss:
            self.parse_bool("press_move", uss["press_move"])

        if "at_color" in uss:
            self.parse_color("at_color", uss["at_color"])
        
        if "ia_color" in uss:
            self.parse_color("ia_color", uss["ia_color"])
        
        if "vb_color" in uss:
            self.parse_color("vb_color", uss["vb_color"])
        
        if "vs_color" in uss:
            self.parse_color("vs_color", uss["vs_color"])
        
        if "st_color" in uss:
            self.parse_color("st_color", uss["st_color"])
        
        if "it_color" in uss:
            self.parse_color("it_color", uss["it_color"])
        
        if "half_sp" in uss:
            self.parse_num("half_sp", uss["half_sp"], int, (0, 50), int)
        
        if "graph_types" in uss:
            self.parse_selection_list("graph_types", uss["graph_types"], int, 4, list(range(8)))
        
        if "graph_chls" in uss:
            self.parse_selection_list("graph_chls", uss["graph_chls"], int, 4, list(range(4)))
        
        if "zoom_step" in uss:
            self.parse_num("zoom_step", uss["zoom_step"], (int, float), (1.0, 10.0), float)

        if "move_step" in uss:
            self.parse_num("move_step", uss["move_step"], int, (1, 500), int)

        if "select_dist" in uss:
            self.parse_num("select_dist", uss["select_dist"], int, (1, 100), int)
    
    def parse_range(self, name, value, dtype, target_range, target_dtype):
        if name in self._setti:
            if isinstance(value, (tuple, list)) and len(value) == 2 and isinstance(value[0], dtype) and isinstance(value[1], dtype):
                if target_range[0] <= value[0] <= target_range[1] and target_range[0] <= value[1] <= target_range[1]:
                    if value[0] < value[1]:
                        self._setti[name] = (target_dtype(value[0]), target_dtype(value[1]))

    def parse_selection(self, name, value, value_list):
        if name in self._setti:
            if isinstance(value, str) and value.lower() in value_list:
                self._setti[name] = str(value)
    
    def parse_selection_list(self, name, value, dtype, length, value_list):
        if name in self._setti:
            if isinstance(value, (tuple, list)) and len(value) == length:
                parsed_list = []
                for i in value:
                    if isinstance(i, dtype) and i in value_list:
                        parsed_list.append(i)
                    else:
                        return
                self._setti[name] = parsed_list
    
    def parse_num(self, name, value, dtype, target_range, target_dtype):
        if name in self._setti:
            if isinstance(value, dtype) and target_range[0] <= value <= target_range[1]:
                self._setti[name] = target_dtype(value)
    
    def parse_bool(self, name, value):
        if name in self._setti:
            if isinstance(value, (bool, int)):
                self._setti[name] = bool(value)
    
    def parse_color(self, name, value):
        if name in self._setti:
            if isinstance(value, (tuple, list)) and len(value) == 3 and isinstance(value[0], int) and isinstance(value[1], int) and isinstance(value[2], int):
                if 0 <= value[0] <= 255 and 0 <= value[2] <= 255 and 0 <= value[2] <= 255:
                    self._setti[name] = tuple(value)
