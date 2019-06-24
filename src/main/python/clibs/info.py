# -*- coding: utf-8 -*-

__info__ = """
Current stable version:

Current alpha version:

Current version:
v1.0.9-beta
Website:
https://github.com/liujiacode/DigitalPalette
Date:
2019.06.24
"""

def current_version():
    version = __info__.split("\n")[-6]
    return version

def compatible_versions():
    return (r"^v1.0*", )

def website():
    return __info__.split("\n")[-4]

def update_date():
    return __info__.split("\n")[-2]
