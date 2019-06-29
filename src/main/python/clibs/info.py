# -*- coding: utf-8 -*-

import re


def current_version():
    return "v1.0.18-beta"

def website():
    return "https://github.com/liujiacode/DigitalPalette"

def update_date():
    return "2019.06.29"

def if_version_compatible(version):
    version_cmp = False
    for vre in (r"^v1\.[0].*", ):
        if re.match(vre, version):
            a = re.match(vre, version)
            version_cmp = True
            break

    return version_cmp


if __name__ == "__main__":
    assert if_version_compatible("v1.0.0-beta") == True
    assert if_version_compatible("v1.0.1-beta") == True
    assert if_version_compatible("v1.0.1-xxxx") == True
    assert if_version_compatible("v1.1.0-beta") == False
    assert if_version_compatible("x1.0.0-beta") == False
