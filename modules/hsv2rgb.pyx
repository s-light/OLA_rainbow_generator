#!/usr/bin/env python2
# coding=utf-8

"""
hsv2rgb.

function should return rgb value for hsv input.
the rainbow could be calculated in two ways.
just use the python internal hsv2rgb from colorsys
nicer option:
FastLED hsv2rgb_rainbow with visually balanced rainbow
https://github.com/FastLED/FastLED/blob/master/hsv2rgb.h#L18
https://github.com/FastLED/FastLED/blob/master/hsv2rgb.cpp#L278

this is partial port from hsv2rgb.cpp to python/cython


original description from hsv2rgb.cpp:
Functions to convert HSV colors to RGB colors.

The basically fall into two groups: spectra, and rainbows.
Spectra and rainbows are not the same thing.  Wikipedia has a good
illustration here
http://upload.wikimedia.org/wikipedia/commons/f/f6/Prism_compare_rainbow_01.png
from this article
http://en.wikipedia.org/wiki/Rainbow#Number_of_colours_in_spectrum_or_rainbow
that shows a 'spectrum' and a 'rainbow' side by side.  Among other
differences, you'll see that a 'rainbow' has much more yellow than
a plain spectrum.  "Classic" LED color washes are spectrum based, and
usually show very little yellow.

Wikipedia's page on HSV color space, with pseudocode for conversion
to RGB color space
http://en.wikipedia.org/wiki/HSL_and_HSV
Note that their conversion algorithm, which is (naturally) very popular
is in the "maximum brightness at any given hue" style, vs the "uniform
brightness for all hues" style.

You can't have both; either purple is the same brightness as red, e.g
red = #FF0000 and purple = #800080 -> same "total light" output
OR purple is 'as bright as it can be', e.g.
red = #FF0000 and purple = #FF00FF -> purple is much brighter than red.
The colorspace conversions here try to keep the apparent brightness
constant even as the hue varies.

Adafruit's "Wheel" function, discussed here
http://forums.adafruit.com/viewtopic.php?f=47&t=22483
is also of the "constant apparent brightness" variety.

TODO: provide the 'maximum brightness no matter what' variation.

See also some good, clear Arduino C code from Kasper Kamperman
http://www.kasperkamperman.com/blog/arduino/arduino-programming-hsb-to-rgb/
which in turn was was based on Windows C code from "nico80"
http://www.codeproject.com/Articles/9207/An-HSB-RGBA-colour-picker



Original Source:
The MIT License (MIT)

Copyright (c) 2013 FastLED

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


# def hsv2rgb_rainbow( int hue, int satturation, int value, CRGB& rgb) {
# def hsv2rgb_rainbow( const CHSV& hsv, CRGB& rgb) {
def hsv2rgb_rainbow_8bit(hue, sat, val):
    """Convert hsv to rgb in an visual balanced way (8bit variant)."""
    # constants
    K255 = 255
    K171 = 171
    K170 = 170
    K85 = 85

    # Yellow has a higher inherent brightness than
    # any other color; 'pure' yellow is perceived to
    # be 93% as bright as white.  In order to make
    # yellow appear the correct relative brightness,
    # it has to be rendered brighter than all other
    # colors.
    # Level Y1 is a moderate boost, the default.
    # Level Y2 is a strong boost.
    # const uint8_t Y1 = 1
    # const uint8_t Y2 = 0
    Y1 = 1
    Y2 = 0

    # G2: Whether to divide all greens by two.
    # Depends GREATLY on your particular LEDs
    # const uint8_t G2 = 0
    G2 = 0

    # Gscale: what to scale green down by.
    # Depends GREATLY on your particular LEDs
    # const uint8_t Gscale = 0
    Gscale = 0

    # uint8_t hue = hsv.hue;
    # uint8_t sat = hsv.sat;
    # uint8_t val = hsv.val;

    # uint8_t offset = hue & 0x1F; 0..31
    offset = hue & 0x1F

    # uint8_t offset8 = offset
    offset8 = offset * 8
    # offset8 = offset
    # offset8 <<= 3

    # uint8_t third = scale8( offset8, (256 / 3)); max = 85
    third = scale8(offset8, (256 // 3))

    # uint8_t r, g, b;
    r = 0
    g = 0
    b = 0

    if(not(hue & 0x80)):
        # 0XX
        if(not(hue & 0x40)):
            # 00X
            # section 0-1
            if(not(hue & 0x20)):
                # 000
                # case 0: R -> O
                r = K255 - third
                g = third
                b = 0
                # FORCE_REFERENCE(b)
            else:
                # 001
                # case 1: O -> Y
                if(Y1):
                    r = K171
                    g = K85 + third
                    b = 0
                    # FORCE_REFERENCE(b)
                if(Y2):
                    r = K170 + third
                    # uint8_t twothirds = (third << 1)
                    # uint8_t twothirds = scale8( offset8, ((256 * 2) / 3))
                    # --> max=170
                    twothirds = scale8(offset8, ((256 * 2) // 3))
                    g = K85 + twothirds
                    b = 0
                    # FORCE_REFERENCE(b)
        else:
            # 01X
            # section 2-3
            if(not (hue & 0x20)):
                # 010
                # case 2: Y -> G
                if(Y1):
                    # uint8_t twothirds = (third << 1)
                    # uint8_t twothirds = scale8( offset8, ((256 * 2) / 3))
                    # --> max=170
                    twothirds = scale8(offset8, ((256 * 2) // 3))
                    r = K171 - twothirds
                    g = K170 + third
                    b = 0
                    # FORCE_REFERENCE(b)
                if(Y2):
                    r = K255 - offset8
                    g = K255
                    b = 0
                    # FORCE_REFERENCE(b)
            else:
                # 011
                # case 3: G -> A
                r = 0
                # FORCE_REFERENCE(r)
                g = K255 - third
                b = third
    else:
        # section 4-7
        # 1XX
        if(not (hue & 0x40)):
            # 10X
            if(not (hue & 0x20)):
                # 100
                # case 4: A -> B
                r = 0
                # FORCE_REFERENCE(r)
                # uint8_t twothirds = (third << 1)
                # uint8_t twothirds = scale8( offset8, ((256 * 2) / 3)) max=170
                twothirds = scale8(offset8, ((256 * 2) // 3))
                g = K171 - twothirds
                # K170?
                b = K85 + twothirds
            else:
                # 101
                # case 5: B -> P
                r = third
                g = 0
                # FORCE_REFERENCE(g)
                b = K255 - third
        else:
            if(not (hue & 0x20)):
                # 110
                # case 6: P -- K
                r = K85 + third
                g = 0
                # FORCE_REFERENCE(g)
                b = K171 - third

            else:
                # 111
                # case 7: K -> R
                r = K170 + third
                g = 0
                # FORCE_REFERENCE(g)
                b = K85 - third

    # This is one of the good places to scale the green down,
    # although the client can scale green down as well.
    if(G2):
        g = g >> 1
    if(Gscale):
        g = scale8_video(g, Gscale)

    # Scale down colors if we're desaturated at all
    # and add the brightness_floor to r, g, and b.
    if(sat != 255):
        if(sat == 0):
            r = 255
            b = 255
            g = 255
        else:
            # nscale8x3_video( r, g, b, sat);
            if(r):
                r = scale8(r, sat)
            if(g):
                g = scale8(g, sat)
            if(b):
                b = scale8(b, sat)

            # uint8_t desat = 255 - sat
            desat = 255 - sat
            desat = scale8(desat, desat)

            # uint8_t brightness_floor = desat
            brightness_floor = desat
            r += brightness_floor
            g += brightness_floor
            b += brightness_floor

    # Now scale everything down if we're at value < 255.
    if(val != 255):
        val = scale8_video(val, val)
        if(val == 0):
            r = 0
            g = 0
            b = 0
        else:
            # nscale8x3_video( r, g, b, val);
            if(r):
                r = scale8(r, val)
            if(g):
                g = scale8(g, val)
            if(b):
                b = scale8(b, val)

    # rgb = RGB()
    # rgb.r = r
    # rgb.g = g
    # rgb.b = b
    # return rgb
    return (r, g, b)


def scale8(i, scale):
    """Scale in 8bit."""
    # return (((uint16_t)i) * (1+(uint16_t)(scale))) >> 8;
    return (i * (1 + scale)) >> 8


# LIB8STATIC_ALWAYS_INLINE uint8_t scale8_video( uint8_t i, fract8 scale)
def scale8_video(i, scale):
    """
    Video scale version.

    The "video" version of scale8 guarantees that the output will
    be only be zero if one or both of the inputs are zero.  If both
    inputs are non-zero, the output is guaranteed to be non-zero.
    This makes for better 'video' LED dimming, at the cost of
    several additional cycles.
    """
    # uint8_t j = (((int)i * (int)scale) >> 8) + ((i&&scale)?1:0);
    # uint8_t nonzeroscale = (scale != 0) ? 1 : 0;
    # uint8_t j = (i == 0) ? 0 : (((int)i * (int)(scale) ) >> 8) +nonzeroscale;
    # return j;
    nonzeroscale = 0
    if scale != 0:
        nonzeroscale = 1
    if i == 0:
        j = 0
    else:
        # j = (((int)i * (int)(scale) ) >> 8) + nonzeroscale
        j = ((i * scale) >> 8) + nonzeroscale
    return j
