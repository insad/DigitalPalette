# -*- coding: utf-8 -*-

from clibs import info as dpinfo
import os
import json
import re


class Argument(object):
    """
    Argument object. Manage setting args.
    """

    def __init__(self, default_settings, settings_dir, langs_dir):
        """
        Load initial settings.
        """

        self.hm_rules = ("analogous", "monochromatic", "triad", "tetrad", "pentad", "complementary", "shades", "custom")
        self.lang = ("en", "zh_cn")

        store = settings_dir

        if not os.path.isdir(store):
            os.makedirs(store)

        self._store = os.sep.join((store, "settings.json"))

        # loading langs.
        self.global_langs = (
            "en", "ar", "be", "bg", "ca", "cs", "da", "de", "el", "es", 
            "et", "fi", "fr", "hr", "hu", "is", "it", "iw", "ja", "ko", 
            "lt", "lv", "mk", "nl", "no", "pl", "pt", "ro", "ru", "sh", 
            "sk", "sl", "sq", "sr", "sv", "th", "tr", "uk", "zh"
        )

        lang_paths = [(39, "default"),]
        if os.path.isdir(langs_dir):
            for lang in os.listdir(langs_dir):
                if lang.split(".")[-1] == "qm" and os.path.isfile(os.sep.join((langs_dir, lang))):
                    glang = re.split("\.|_|-", lang)[0]
                    if glang in self.global_langs:
                        lang_paths.append((self.global_langs.index(glang), os.sep.join((langs_dir, lang))))
        else:
            os.makedirs(langs_dir)

        self.lang_paths = tuple(lang_paths)

        # parse the default lang path before loading.
        _default_settings = list(default_settings)
        _default_settings[21] = self.parse_lang(_default_settings[21], by_idx=False)
        self.default_settings = tuple(_default_settings)

        self.err = None

        if os.path.isfile(self._store):
            uss = []
            with open(self._store, "r") as sf:
                try:
                    uss = json.load(sf)
                except:
                    self.err = (3, "")
                    uss = []
                
                if not isinstance(uss, (tuple, list)):
                    self.err = (3, "")
                    uss = []
            
            lst = []
            if uss:
                if dpinfo.if_version_compatible(uss[-1]):
                    try:
                        lst = self.load_settings(uss)
                    except Exception as erro:
                        self.err = (1, str(erro))
                else:
                    self.err = (2, str(uss[-1]))

            if self.err:
                self.settings = tuple(list(self.default_settings) + [dpinfo.current_version(),])
            else:
                self.settings = tuple(lst + [dpinfo.current_version(),])
        
        else:
            self.settings = tuple(list(self.default_settings) + [dpinfo.current_version(),])

    def reset_settings(self):
        self.settings = tuple(list(self.default_settings) + [dpinfo.current_version(),])

    def modify_settings(self, idx_values):
        lst = list(self.settings)

        err_lst = []
        for idx, value in idx_values:
            try:
                if idx == 0:
                    lst[idx] = self.parse_range(value, (int, float), (0.0, 360.0), float)

                elif idx in (1, 2):
                    lst[idx] = self.parse_range(value, (int, float), (0.0, 1.0), float)

                elif idx in (3, 4, 5, 6, 7):
                    lst[idx] = self.parse_num(value, (int, float), (0.0, 1.0), float)

                elif idx == 8:
                    lst[idx] = self.parse_num(value, (int, float), (1.0, 10.0), float)

                elif idx in (9, 10, 11):
                    lst[idx] = self.parse_num(value, int, (1, 500), int)

                elif idx in (12, 13, 14, 15, 16, 17):
                    lst[idx] = self.parse_color(value)

                elif idx == 18:
                    lst[idx] = self.parse_selection_list(value, int, 4, list(range(8)))

                elif idx == 19:
                    lst[idx] = self.parse_selection_list(value, int, 4, list(range(4)))

                elif idx == 20:
                    lst[idx] = self.parse_selection(value, self.hm_rules)

                elif idx == 21:
                    lst[idx] = self.parse_lang(value, by_idx=True)

                elif idx == 22:
                    lst[idx] = self.parse_bool(value)

                else:
                    raise ValueError("Index out of range.")
            
            except Exception as err:
                err_lst.append((idx, value))
        
        self.settings = tuple(lst)
        return err_lst

    def save_settings(self):
        """
        Save settings to file.
        """

        with open(self._store, "w") as sf:
            json.dump(self.settings, sf, indent=4)

    def load_settings(self, uss):
        """
        Modify default settings by user settings.

        Parameters:
          uss - dict. user settings.
        """

        if len(uss) != 24:
            raise ValueError("settings file length error.")

        lst = []

        lst.append(self.parse_range(uss[0], (int, float), (0.0, 360.0), float))     # "h_range", 
        lst.append(self.parse_range(uss[1], (int, float), (0.0, 1.0), float))       # "s_range", 
        lst.append(self.parse_range(uss[2], (int, float), (0.0, 1.0), float))       # "v_range", 
        lst.append(self.parse_num(uss[3], (int, float), (0.0, 1.0), float))         # "radius", 
        lst.append(self.parse_num(uss[4], (int, float), (0.0, 1.0), float))         # "color_radius", 
        lst.append(self.parse_num(uss[5], (int, float), (0.0, 1.0), float))         # "tip_radius", 
        lst.append(self.parse_num(uss[6], (int, float), (0.0, 1.0), float))         # "widratio", 
        lst.append(self.parse_num(uss[7], (int, float), (0.0, 1.0), float))         # "bar_widratio", 
        lst.append(self.parse_num(uss[8], (int, float), (1.0, 10.0), float))        # "zoom_step", 
        lst.append(self.parse_num(uss[9], int, (1, 500), int))                      # "move_step", 
        lst.append(self.parse_num(uss[10], int, (1, 500), int))                     # "select_dist", 
        lst.append(self.parse_num(uss[11], int, (1, 500), int))                     # "half_sp", 
        lst.append(self.parse_color(uss[12]))                                       # "at_color", 
        lst.append(self.parse_color(uss[13]))                                       # "ia_color", 
        lst.append(self.parse_color(uss[14]))                                       # "vb_color", 
        lst.append(self.parse_color(uss[15]))                                       # "vs_color", 
        lst.append(self.parse_color(uss[16]))                                       # "st_color", 
        lst.append(self.parse_color(uss[17]))                                       # "it_color", 
        lst.append(self.parse_selection_list(uss[18], int, 4, list(range(8))))      # "graph_types", 
        lst.append(self.parse_selection_list(uss[19], int, 4, list(range(4))))      # "graph_chls", 
        lst.append(self.parse_selection(uss[20], self.hm_rules))                    # "hm_rule", 
        lst.append(self.parse_lang(uss[21], by_idx=False))                          # "lang", 
        lst.append(self.parse_bool(uss[22]))                                        # "press_move", 
    
        return lst

    def parse_range(self, value, dtype, target_range, target_dtype):
        if isinstance(value, (tuple, list)) and len(value) == 2 and isinstance(value[0], dtype) and isinstance(value[1], dtype):
            if target_range[0] <= value[0] <= target_range[1] and target_range[0] <= value[1] <= target_range[1]:
                if value[0] < value[1]:
                    return (target_dtype(value[0]), target_dtype(value[1]))

        raise ValueError("parse_range failed.")

    def parse_selection(self, value, value_list):
        if isinstance(value, str):
            if value.lower() in value_list:
                return value.lower()
        
        raise ValueError("parse_selection failed.")

    def parse_selection_list(self, value, dtype, length, value_list):
        if isinstance(value, (tuple, list)) and len(value) == length:
            parsed_list = []
            for i in value:
                if isinstance(i, dtype) and i in value_list:
                    parsed_list.append(i)
                else:
                    raise ValueError("parse_selection_list failed.")
            
            return parsed_list
        
        raise ValueError("parse_selection_list failed.")
    
    def parse_num(self, value, dtype, target_range, target_dtype):
        if isinstance(value, dtype) and target_range[0] <= value <= target_range[1]:
            return target_dtype(value)
        
        raise ValueError("parse_num failed.")
    
    def parse_bool(self, value):
        if isinstance(value, (bool, int)):
            return bool(value)
        
        raise ValueError("parse_bool failed.")
    
    def parse_color(self, value):
        if isinstance(value, (tuple, list)) and len(value) == 3 and isinstance(value[0], int) and isinstance(value[1], int) and isinstance(value[2], int):
            if 0 <= value[0] <= 255 and 0 <= value[2] <= 255 and 0 <= value[2] <= 255:
                return tuple(value)
        
        raise ValueError("parse_color failed.")

    def parse_lang(self, value, by_idx=False):
        lang_lst = (0, "default")

        if isinstance(value, (tuple, list)):
            for i in range(len(self.lang_paths) - 1):
                lang_name = os.path.basename(self.lang_paths[i + 1][1]).split(".")[0]
                if by_idx:
                    if value[0] == i + 1:
                        lang_lst = (i + 1, lang_name)
                        break
                else:
                    if value[1] == lang_name:
                        lang_lst = (i + 1, lang_name)
                        break
            
        return lang_lst
