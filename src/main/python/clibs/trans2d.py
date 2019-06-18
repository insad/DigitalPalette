# -*- coding: utf-8 -*-

import numpy as np


def rotate_point(point, theta, dtype=int):
    """
    Rotate point in anti-clockwise direction. Rotating center is (0, 0), theta is in angle type and r_theta is in radian type.

    Parameters:
      point - numpy.ndarray. point for rotating.
      theta - float. rotating angle (in angle type).
    
    Returns:
      rotated point.
    """

    r_theta = theta * np.pi / 180
    Rz = np.array([[np.cos(r_theta), np.sin(r_theta) * -1],
                   [np.sin(r_theta), np.cos(r_theta),    ]])
    _pt = Rz.dot(point)
    return _pt.astype(dtype)

def rotate_point_center(center, point, theta, dtype=int):
    """
    Rotate point in anti-clockwise direction around given center.

    Parameters:
      center - numpy.ndarray. rotating center.
      point - numpy.ndarray. point for rotating.
      theta - float. rotating angle (in angle type).
    
    Returns:
      rotated point.
    """

    delta_point = point - center
    rotated_point = rotate_point(delta_point, theta)
    _pt = rotated_point + np.array(center)
    return _pt.astype(dtype)

def get_theta(point):
    """
    Get angle between point and x axis in anti-clockwise direction. Center is (0, 0).

    Parameters:
      point - numpy.ndarray. rotated point.
    
    Returns:
      rotated theta.
    """

    delta_x = point[0]
    delta_y = point[1]

    if delta_x == 0:
        if delta_y > 0:
            hue = 90
        else:
            hue = 270
    else:
        _hue = np.arctan(delta_y / delta_x) * 180 / np.pi
        if delta_x > 0:
            hue = _hue if _hue > 0 else 360 + _hue
        else:
            hue = _hue + 180

    return hue

def get_theta_center(center, point):
    """
    Get angle between point and x axis in anti-clockwise direction around given center.

    Parameters:
      center - numpy.ndarray. rotating center.
      point - numpy.ndarray. rotated point.
    
    Returns:
      rotated theta.
    """

    delta_point = point - center
    return get_theta(delta_point)

def get_outer_box(center, radius, dtype=int):
    """
    Get outer box of circle with raduis.

    Parameters:
      center - numpy.ndarray. circle center.
      radius - float. circle radius.
    
    Returns:
      box.
    """

    return np.array((center[0] - radius, center[1] - radius, 2 * radius, 2 * radius), dtype=dtype)
