# -*- coding: utf-8 -*-

import re
import urllib


def current_version():
    return "v1.0.14-beta"

def website():
    return "https://github.com/liujiacode/DigitalPalette"

def update_date():
    return "2019.06.26"

def if_version_compatible(version):
    version_cmp = False
    for vre in (r"^v1\.[0].*", ):
        if re.match(vre, version):
            a = re.match(vre, version)
            version_cmp = True
            break

    return version_cmp

def about_info():
    info = """
DigitalPalette Info

    --------------
    Version : {}
    Author  : Liu Jia
    Update  : {}
    Github  : {}
    --------------

DigitalPalette is free software, which is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. You can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation. See the GNU General Public License for more details.
    """.format(current_version(), update_date(), website())

    return info


if __name__ == "__main__":
    assert if_version_compatible("v1.0.0-beta") == True
    assert if_version_compatible("v1.0.1-beta") == True
    assert if_version_compatible("v1.0.1-xxxx") == True
    assert if_version_compatible("v1.1.0-beta") == False
    assert if_version_compatible("x1.0.0-beta") == False
