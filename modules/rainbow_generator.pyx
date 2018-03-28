#!/usr/bin/env python2
# coding=utf-8

"""
ola test pattern generator.

    generates some test patterns.
    todo:
        ~ all fine :-)
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


import time
import array
import json

import configdict
from olathreaded import OLAThread
# from olathreaded import OLAThread_States
from exception_classes import FormatError

from rainbow import get_rgb_from_rainbow
import int_math


##########################################
# classes


class RainbowGenerator(OLAThread):
    """Class that extends on OLAThread and generates the pattern."""

    channels_per_pixel = 4

    config_defaults = {
        'generator': {
            'update_interval': 100,
            'brightness': 255,
            'pixel_count': 50,
            'universe': 1,
            'pattern': {
                # pattern loop duration in milli seconds
                'duration': 10000,
                # 'current_position': 0,
                'running': True,
            },
            # 'repeat_count': 4,
            # 'repeat_snake': True,
            # "color_channels": [
            #     "red",
            #     "green",
            #     "blue",
            # ],
        },
        # 'patch': {
        # },
    }

    def __init__(self, config, verbose=False):
        """Init mapper things."""
        # super(OLAThread, self).__init__()
        OLAThread.__init__(self)
        self.verbose = verbose

        # extend config with defaults
        self.config = config
        configdict.extend_deep(self.config, self.config_defaults.copy())

        if self.verbose:
            print("RainbowGenerator config: {}".format(
                json.dumps(
                    self.config,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                )
            ))

        self._pixel_count = 50
        self._brightness = 255
        self._universe = 1

        self._init_pattern()

        if self.verbose:
            print("--> finished.")
            # print("config: {}".format(self.config))

    def _init_pattern(self):
        """Load and initialize all available patterns."""
        if self.verbose:
            print("init pattern..")
        # initialize properties
        self.pixel_count = self.config['generator']['pixel_count']
        # --> this also initializes the data_output array.
        # with this brightness we make sure that the value bounds are met
        self.brightness = self.config['generator']['brightness']
        self.universe = self.config['generator']['universe']
        self.loop_start = time.time()

    def ola_connected(self):
        """Register update event callback and switch to running mode."""
        self.wrapper.AddEvent(
            self.config['generator']['update_interval'],
            self._generate_pattern
        )
        # python3 syntax
        # super().ola_connected()
        # python2 syntax
        # super(OLAThread, self).ola_connected()
        # explicit call
        OLAThread.ola_connected(self)

    ##########################################

    def _update_array(self):
        """Update output array."""
        # prepare temp array
        self.data_output = array.array('B')
        self.data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        self.data_output *= self._channel_count

    def _update_brightness(self):
        """Update brightness settings in array."""
        for ch_index in range(0, self._channel_count, 4):
            self.data_output[ch_index] = self.brightness

    ##########################################

    @property
    def pixel_count(self):
        """Pixel count."""
        return self._pixel_count

    @pixel_count.setter
    def pixel_count(self, value):
        try:
            value = int(value)
        except Exception:
            raise FormatError(
                "int",
                "could not interpret input as integer",
                value
            )
        else:
            if (value >= 0) and (value <= 128):
                self._pixel_count = value
                self._channel_count = (
                    self._pixel_count * self.channels_per_pixel
                )
                self.config['generator']['pixel_count'] = self._pixel_count
                self._update_array()
                self._update_brightness()
            else:
                raise FormatError(
                    "int",
                    "Format not valid. pixel_count must be > 0 and <= 128",
                    value
                )

    @property
    def brightness(self):
        """brightness."""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        try:
            value = int(value)
        except Exception:
            raise FormatError(
                "int",
                "could not interpret input as integer",
                value
            )
        else:
            if (value >= 0) and (value <= 255):
                self._brightness = value
                self.config['generator']['brightness'] = self._brightness
                self._update_brightness()
            else:
                raise FormatError(
                    "int",
                    "Format not valid. brightness must be > 0 and <= 255",
                    value
                )

    @property
    def universe(self):
        """Universe."""
        return self._universe

    @universe.setter
    def universe(self, value):
        try:
            value = int(value)
        except Exception:
            raise FormatError(
                "int",
                "could not interpret input as integer",
                value
            )
        else:
            if (value >= 0) and (value <= 4000):
                self._universe = value
                self.config['generator']['universe'] = self._universe
            else:
                raise FormatError(
                    "int",
                    "Format not valid. universe must be > 0 and <= 4000",
                    value
                )

    ##########################################

    # def _handle_repeat(self, channels):
    #     """Handle all pattern repeating things."""
    #     # this does not work. we have to use the pixel information.
    #     # otherwiese color-order will get mixed up..
    #     # pixel_count = self.config['generator']['pixel_count']
    #     repeat_count = self.config['generator']['repeat_count']
    #     repeat_snake = self.config['generator']['repeat_snake']
    #     channels_count = len(channels)
    #     # print("pixel_count:", pixel_count)
    #     # print("repeat_snake:", repeat_snake)
    #     # print("repeat_count:", repeat_count)
    #
    #     if repeat_count > 0:
    #         for repeate_index in range(1, repeat_count):
    #             # print("repeate_index:", repeate_index)
    #             # normal direction
    #             # = snake forward
    #             pixel_range = range(0, channels_count)
    #             # if repeat_snake and ((repeate_index % 2) > 0):
    #             if repeat_snake:
    #                 # print("repeat_snake:", repeat_snake)
    #                 if ((repeate_index % 2) > 0):
    #                     # print("(repeate_index % 2):", (repeate_index % 2))
    #                     # snake back
    #                     pixel_range = range(channels_count - 1, -1, -1)
    #             # print("pixel_range:", pixel_range)
    #             for channel_index in pixel_range:
    #                 # print("append:", channel_index)
    #                 try:
    #                     value = channels[channel_index]
    #                 except Exception as e:
    #                     print('error:', e)
    #                 else:
    #                     channels.append(value)
    #     return channels

    def _generate_pattern(self):
        """Generate pattern data."""
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(
            self.config['generator']['update_interval'],
            self._generate_pattern
        )

        if self.config['generator']['pattern']['running']:
            # update data
            loop_duration = self.config['generator']['pattern']['duration']
            current_duration = int((time.time() - self.loop_start) * 1000)
            # print(
            #     "loop_duration: {} \t"
            #     "current_duration: {}".format(
            #         loop_duration,
            #         current_duration
            #     )
            # )
            # handle current_duration
            if current_duration >= loop_duration:
                self.loop_start = time.time()
                current_duration = 0
                # print("loop restart")

            offset_8bit = int_math.map_bound_8bit(
                current_duration,
                loop_duration
            )
            pixel_count = self.pixel_count

            for pixel_index in range(0, pixel_count):
                # rgb = get_rgb_from_rainbow(
                #     pixel_index,
                #     pixel_count,
                #     offset,
                #     offset_max
                # )
                rgb = get_rgb_from_rainbow(
                    pixel_index,
                    pixel_count,
                    offset_8bit
                )
                ch_index = pixel_index * 4
                # add offset for pixel-brightness value
                ch_index += 1
                self.data_output[ch_index + 0] = rgb[0]
                self.data_output[ch_index + 1] = rgb[1]
                self.data_output[ch_index + 2] = rgb[2]

            # handle repeate
            # TODO

            # send frame
            self.dmx_send_frame(self.universe, self.data_output)


##########################################
if __name__ == '__main__':
    import sys
    print(42 * '*')
    print('Python Version: ' + sys.version)
    print(42 * '*')
    print(__doc__)
    print(42 * '*')
    print("This Module has no stand alone functionality.")
    print(42 * '*')

##########################################
