# -*- coding: utf-8 -*-

import binascii


def export_swatch(color_list):
    """
    Export color set list in swatch type (for Adobe and GIMP exchange).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc), ...]}

    Returns:
        Binary strings.
    """

    swatch_chars_v1 = "0001{:0>4x}".format(len(color_list) * 5)
    swatch_chars_v2 = "0002{:0>4x}".format(len(color_list) * 5)

    for idx in range(len(color_list)):
        for i in (2, 1, 0, 3, 4):
            h, s, v = color_list[idx][0][i].hsv
            pr_chars = "0001{:0>4x}{:0>4x}{:0>4x}0000".format(int(h * 182.04167), int(s * 65535), int(v * 65535))
            swatch_chars_v1 += pr_chars

            swatch_chars_v2 += pr_chars

            name = "DigiPale-{}-{}".format(idx, i)
            swatch_chars_v2 += "0000{:0>4x}".format(len(name) + 1)

            for n in name:
                swatch_chars_v2 += "{:0>4x}".format(ord(n))

            swatch_chars_v2 += "0000"

    swatch_chars = swatch_chars_v1 + swatch_chars_v2

    return binascii.a2b_hex(swatch_chars)

def export_text(color_list):
    """
    Export color set list in plain text (for directly reading).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc), ...]}

    Returns:
        Plain text strings.
    """

    plain_text = ""

    for idx in range(len(color_list)):
        plain_text += "# Name: {}\n".format("DigiPale-{}".format(idx))
        plain_text += "# Rule: {}\n".format(color_list[idx][1])
        plain_text += "{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}{:<8}\n".format("# Index", "R", "G", "B", "H", "S", "V", "Hex Code")

        for i in (2, 1, 0, 3, 4):
            r, g, b = color_list[idx][0][i].rgb
            h, s, v = color_list[idx][0][i].hsv
            hex_code = "#{}".format(color_list[idx][0][i].hec)
            plain_text += "  {:<6}{:<8}{:<8}{:<8}{:<8.2f}{:<8.2f}{:<8.2f}{:<8}\n".format(i, r, g, b, h, s, v, hex_code)

        plain_text += "\n"

    return plain_text

def export_list(color_list):
    """
    Export color set list in list type (for DigitalPalette output).

    Args:
        color_list (tuple or list): [(color_set, hm_rule, name, desc), ...]}

    Returns:
        Json List.
    """

    expt_list = []

    for color in color_list:
        color_dict = {"rule": color[1], "name": color[2], "desc": color[3]}

        for i in (2, 1, 0, 3, 4):
            color_dict["color_{}".format(i)] = color[0][i].export()

        expt_list.append(color_dict)

    return expt_list
