#!/usr/bin/env python2
# coding=utf-8

"""
Rainbow.

Create a nice rainbow pattern.
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


# classes

class RGB(object):
    """Holds one RGB value."""

    def __init__(self, red=0, green=0, blue=0):
        """Initialize with optional values."""
        super(RGB, self).__init__()
        self.red = red
        self.green = green
        self.blue = blue
