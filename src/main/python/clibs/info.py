# -*- coding: utf-8 -*-


__info__ = """
Latest stable version:


Latest alpha version:


Current version:
v1.0.12-beta

Website:
https://github.com/liujiacode/DigitalPalette

Date:
2019.06.25
"""


def current_version():
    version = __info__.split("\n")[-8]
    return version

def compatible_versions():
    return (r"^v1.0*", )

def website():
    return __info__.split("\n")[-5]

def update_date():
    return __info__.split("\n")[-2]
