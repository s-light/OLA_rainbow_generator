#!/usr/bin/env python2
# coding=utf-8

"""
Rainbow.

function should return rgb value for specific position of rainbow.
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


from hsv2rgb import hsv2rgb_rainbow_8bit

import int_math


def get_rgb_from_rainbow(
    pixel,
    pixel_count,
    offset,
    # offset_max=255,
    sat=255,
    val=255
):
    """Calculate RGB value in Rainbow for specified position and offset."""
    # currently hue range is 0..255
    # so we have to map the input values to this range.
    pixel_8bit = int_math.map_bound_8bit(pixel, pixel_count)
    # offset_8bit = int_math.map_bound_8bit(offset, offset_max)
    # hue = pixel_8bit + offset_8bit
    hue = pixel_8bit + offset
    # handle wrap-around
    if hue > 255:
        hue = hue - 256

    return hsv2rgb_rainbow_8bit(hue, sat, val)
