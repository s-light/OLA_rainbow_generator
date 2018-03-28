#!/usr/bin/env python2
# coding=utf-8

"""
Rainbow.

function should return rgb value for specific position of rainbow.
the rainbow could be calculated in two ways.
just use the python internal hsv2rgb from colorsys
or the nicer variant would be to use the
FastLED hsv2rgb_rainbow with visually balanced rainbow
https://github.com/FastLED/FastLED/blob/master/hsv2rgb.h#L18
https://github.com/FastLED/FastLED/blob/master/hsv2rgb.cpp#L278
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


from hsv2rgb import hsv2rgb_rainbow_8bit


def get_rgb_from_rainbow(
    pixel,
    pixel_count,
    offset,
    offset_max
):
    """Calculate RGB value in Rainbow for specified position."""
    pass
    hue = 0
    sat = 0
    val = 0
    return hsv2rgb_rainbow_8bit(hue, sat, val)
