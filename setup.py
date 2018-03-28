#!/usr/bin/env python2
# coding=utf-8

"""Setup things :-) ."""

# usage:
# python ./setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("hsv2rgb.pyx", "rainbow.pyx")
)
