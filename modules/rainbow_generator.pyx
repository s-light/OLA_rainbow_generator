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
# from cython cimport array
# import json

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
                'duration_ms': 10000,
                # 'current_position': 0,
                'running': True,
            },
            'repeat_count': 4,
            'repeat_snake': True,
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

        # if self.verbose:
        #     print("RainbowGenerator config: {}".format(
        #         json.dumps(
        #             self.config,
        #             sort_keys=True,
        #             indent=4,
        #             separators=(',', ': ')
        #         )
        #     ))

        self._pixel_count = 50
        self._brightness = 255
        self._pattern_duration = 10000
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
        gen_config = self.config['generator']
        self.pixel_count = gen_config['pixel_count']
        # --> this also initializes the data_output array.
        # with this brightness we make sure that the value bounds are met
        self.brightness = gen_config['brightness']
        self.universe = gen_config['universe']
        self.pattern_duration = gen_config['pattern']['duration_ms'] // 1000
        self.loop_start = time.time()

    def ola_connected(self):
        """Register update event callback and switch to running mode."""
        self.wrapper.AddEvent(
            self.config['generator']['update_interval'],
            self._update
        )
        # python3 syntax
        # super().ola_connected()
        # python2 syntax
        # super(OLAThread, self).ola_connected()
        # explicit call
        OLAThread.ola_connected(self)

    ##########################################

    def _init_array(self):
        """Init output array."""
        self.data_output = array.array('B')
        self.data_output.append(0)
        # multiply so we have a array with total_channel_count zeros in it:
        # this is much faster than a for loop!
        self.data_output *= self._channel_count
        # prepare snaked array
        self.data_snaked = array.array('B')
        self.data_snaked.append(0)
        self.data_snaked *= self._channel_count

    def _update_array_size(self):
        """Update output array."""
        # cython
        # array.resize(self.data_output, self._channel_count)
        # array.resize(self.data_snaked, self._channel_count)
        # pure python
        self._init_array()

    def _update_brightness(self):
        """Update brightness settings in array."""
        for ch_index in range(0, self._channel_count, 4):
            self.data_output[ch_index] = self.brightness

    ##########################################

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

    @property
    def update_interval(self):
        """update_interval."""
        return self.config['generator']['update_interval']

    @update_interval.setter
    def update_interval(self, value):
        try:
            value = int(value)
        except Exception:
            raise FormatError(
                "int",
                "could not interpret input as integer",
                value
            )
        else:
            if (value >= 0) and (value <= 5000):
                self.config['generator']['update_interval'] = value
            else:
                raise FormatError(
                    "int",
                    "Format not valid. "
                    "update_interval must be > 0 and <= 5000",
                    value
                )

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
                self._update_array_size()
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
    def pattern_duration(self):
        """pattern_duration."""
        return self._pattern_duration_ms // 1000

    @pattern_duration.setter
    def pattern_duration(self, value):
        try:
            value = int(value)
        except Exception:
            raise FormatError(
                "int",
                "could not interpret input as integer",
                value
            )
        else:
            if (value >= 0) and (value <= 3600):
                self._pattern_duration_ms = value * 1000
                self.config['generator']['pattern']['duration_ms'] = \
                    self._pattern_duration_ms
            else:
                raise FormatError(
                    "int",
                    "Format not valid."
                    "pattern_duration must be > 0 and <= 3600 seconds",
                    value
                )

    ##########################################

    def get_pixel_mirror_copy(self, data_input, data_snaked):
        """Create a mirrored copy of data_input (respecting pixels)."""
        for pixel_index in range(0, self.pixel_count):
            ch_index = pixel_index * 4
            # data_input[ch_index + 0] == brightness
            # data_input[ch_index + 1] == red
            # data_input[ch_index + 2] == green
            # data_input[ch_index + 3] == blue
            ch_index_snake = ((self.pixel_count - 1) - pixel_index) * 4
            data_snaked[ch_index_snake + 0] = data_input[ch_index + 0]
            data_snaked[ch_index_snake + 1] = data_input[ch_index + 1]
            data_snaked[ch_index_snake + 2] = data_input[ch_index + 2]
            data_snaked[ch_index_snake + 3] = data_input[ch_index + 3]

    def _handle_repeat(self):
        """Handle all pattern repeating things."""
        repeat_count = self.config['generator']['repeat_count']
        repeat_snake = self.config['generator']['repeat_snake']
        if repeat_snake:
            # generate data
            self.get_pixel_mirror_copy(self.data_output, self.data_snaked)
        if repeat_count > 0:
            for repeate_index in range(1, repeat_count):
                if repeat_snake:
                    if ((repeate_index % 2) > 0):
                        self.dmx_send_frame(
                            self.universe + repeate_index,
                            self.data_snaked
                        )
                    else:
                        self.dmx_send_frame(
                            self.universe + repeate_index,
                            self.data_output
                        )
                else:
                    self.dmx_send_frame(
                        self.universe + repeate_index,
                        self.data_output
                    )
        pass

    def _generate_pattern(self):
        """Generate pattern data."""
        # update data
        loop_duration = self._pattern_duration_ms
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

    def _update(self):
        """Generate pattern data."""
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(
            self.config['generator']['update_interval'],
            self._update
        )

        if self.config['generator']['pattern']['running']:
            self._generate_pattern()

            # send data for first universe
            self.dmx_send_frame(self.universe, self.data_output)

            # handle repeate
            self._handle_repeat()


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
