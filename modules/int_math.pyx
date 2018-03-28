#!/usr/bin/env python2
# coding=utf-8

"""
Integer math.

helper functions for integer math.
"""

# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


def map(value, in_low, in_high, out_low, out_high):
    """
    Map value from on range to another.

    ((value - in_low) * (out_high - out_low)) // (in_high - in_low) + out_low
    """
    # example from /animation_nodes/nodes/number/map_range.py
    # if inMin == inMax:
    #     newValue = 0
    # # with clamping
    #     if inMin < inMax:
    #         _value = min(max(value, inMin), inMax)
    #     else:
    #         _value = min(max(value, inMax), inMin)
    #     with interpolation
    #         newValue = outMin + interpolation(
    #             (_value - inMin) / (inMax - inMin)
    #         ) * (outMax - outMin)
    #     without interpolation
    #         newValue = outMin + (
    #             (_value - inMin) / (inMax - inMin)
    #         ) * (outMax - outMin)
    # # without clamping
    #     newValue = outMin + (
    #         (value - inMin) / (inMax - inMin)
    #     ) * (outMax - outMin)
    # # without clamping - reworded
    # result = (
    #     (
    #         ((value - in_low) / (in_high - in_low)) *
    #         (out_high - out_low)
    #     ) + out_low
    # )

    result = None

    # based on http://arduino.cc/en/Reference/Map
    # and http://stackoverflow.com/a/5650012/574981
    result = (
        (
            ((value - in_low) * (out_high - out_low)) //
            (in_high - in_low)
        ) + out_low
    )

    return result


def map_bound(value, in_low, in_high, out_low, out_high):
    """Map value with high and low bound handling."""
    result = None

    if value <= in_low:
        result = out_low
    else:
        if value >= in_high:
            result = out_high
        else:
            # http://stackoverflow.com/a/5650012/574981
            result = out_low + (
                (out_high - out_low) * (value - in_low) // (in_high - in_low)
            )
    return result


def map_bound_8bit(value, in_high):
    """Map value to 8bit range."""
    result = None

    if value <= 0:
        result = 0
    else:
        if value >= in_high:
            result = 255
        else:
            result = 255 * value // in_high
    return result
