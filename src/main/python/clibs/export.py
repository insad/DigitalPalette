# -*- coding: utf-8 -*-

import binascii


def export_swatch(color_dict):
    """
    Export color set(s) in swatch type (for GIMP file).

    Args:
        color_dict (dict): {"name_0": [hsv_0, hsv_1, hsv_2, hsv_3, hsv_4], ...}

    Returns:
        Binary strings.
    """

    swatch_chars_v1 = "0001{:0>4x}".format(len(color_dict) * 5)
    swatch_chars_v2 = "0002{:0>4x}".format(len(color_dict) * 5)

    for name in color_dict:
        for i in (2, 1, 0, 3, 4):
            h, s, v = color_dict[name][i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), int(s * 65535), int(v * 65535))
            swatch_chars_v1 += pr_chars

            swatch_chars_v2 += pr_chars
            swatch_chars_v2 += "0000{:0>4x}".format(len(name) + 3)

            for n in name +"_{}".format(i):
                swatch_chars_v2 += "{:0>4x}".format(ord(n))

    swatch_chars = swatch_chars_v1 + swatch_chars_v2

    return binascii.a2b_hex(swatch_chars)

def export_text(color_dict):
    """
    Export color set(s) in plain text (for directly reading).

    Args:
        color_dict (dict): {"name_0": [hsv_0, hsv_1, hsv_2, hsv_3, hsv_4], ...}

    Returns:
        Plain text strings.
    """

    plain_text = ""

    for name in color_dict:
        plain_text += "# Name: {}\n".format(name)
        plain_text += "{:<12}{:<10}{:<10}{:<10}{:<12}{:<12}{:<12}{:<8}\n".format("# Index", "R", "G", "B", "H", "S", "V", "Hex code")

        for i in (2, 1, 0, 3, 4):
            r, g, b = color_dict[name][i].rgb
            h, s, v = color_dict[name][i].hsv
            hex_code = "#{}".format(self._color_set[i].hec)
            plain_text += "  {:<10}{:<10}{:<10}{:<10}{:<12.2f}{:<12.2f}{:<12.2f}{:<8}\n".format(i, r, g, b, h, s, v, hex_code)

        plain_text += "\n"

    return plain_text
