# -*- coding: utf-8 -*-

__info__ = """
Latest stable version:


Latest alpha version:


Current version:
v1.0.13-beta

Website:
https://github.com/liujiacode/DigitalPalette

Date:
2019.06.25
"""

import re


def current_version():
    version = __info__.split("\n")[-8]
    return version

def if_version_compatible(version):
    version_cmp = False
    for vre in (r"^v1\.[0].*", ):
        if re.match(vre, version):
            a = re.match(vre, version)
            version_cmp = True
            break

    return version_cmp

def website():
    return __info__.split("\n")[-5]

def update_date():
    return __info__.split("\n")[-2]


if __name__ == "__main__":
    assert if_version_compatible("v1.0.0-beta") == True
    assert if_version_compatible("v1.0.1-beta") == True
    assert if_version_compatible("v1.0.1-xxxx") == True
    assert if_version_compatible("v1.1.0-beta") == False
    assert if_version_compatible("x1.0.0-beta") == False
