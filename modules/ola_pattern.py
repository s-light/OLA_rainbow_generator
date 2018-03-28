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


# import time
import array
import json

import configdict
from olathreaded import OLAThread
# from olathreaded import OLAThread_States
from exception_classes import FormatError


##########################################
# classes


class RainbowGenerator(OLAThread):
    """Class that extends on OLAThread and generates the pattern."""

    channels_per_pixel = 4

    config_defaults = {
        'generator': {
            'update_interval': 100,
            'pattern_duration': 5000,
            'brightness': 255,
            'current_position': 0,
            'pattern_running': True,
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
        """Pixel count."""
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
    #
    # def _apply_pixel_dimmer(self, channels):
    #     """Apply the pixel dimmer for APA102."""
    #     # print("")
    #     global_dimmer_16bit = self.config['generator']['global_dimmer']
    #     # print("global_dimmer_16bit", global_dimmer_16bit)
    #     # 65535 = 255
    #     #  gd   = gd8
    #     # global_dimmer_8bit = 255 * global_dimmer_16bit / 65535
    #     global_dimmer_8bit = pattern.map_16bit_to_8bit(global_dimmer_16bit)
    #     # print("global_dimmer_8bit", global_dimmer_8bit)
    #     # global_dimmer_norm = 1.0 * global_dimmer_16bit / 65535
    #     # print("global_dimmer_norm", global_dimmer_norm)
    #     # print("")
    #     # print(len(channels))
    #     # print(channels)
    #     new_length = (len(channels) / 3) * 4
    #     for i in range(0, new_length, 4):
    #         channels.insert(i, global_dimmer_8bit)
    #         # channels.insert(i + (i * 3), global_dimmer_8bit)
    #     # print(len(channels))
    #     # print(channels)
    #     return channels

    # def _send_universe(self, pattern_name, universe):
    #     """Send one universe of data."""
    #     if pattern_name:
    #         if pattern_name in self.pattern:
    #             # calculate channel values for pattern
    #             channels = self.pattern[pattern_name].
    #             _calculate_step(universe)
    #             # print(42 * '*')
    #             # temp_channel_len = len(channels)
    #             # print('channels len', len(channels))
    #             # print('channels', channels)
    #             # channels_rep = self._handle_repeat(channels)
    #             # print('channels_rep len', len(channels_rep))
    #             # print('channels_rep', channels_rep)
    #             # print("channels len: {:5>}; {:5>}".format(
    #             #     temp_channel_len,
    #             #     len(channels)
    #             # ))
    #             if self.config['generator']['use_pixel_dimming']:
    #                 channels = self._apply_pixel_dimmer(channels)
    #             else:
    #                 channels = self._apply_global_dimmer(channels)
    #             # send frame
    #             self.dmx_send_frame(universe, channels)

    def _generate_pattern(self):
        """Generate pattern data."""
        # register new event (for correct timing as first thing.)
        self.wrapper.AddEvent(
            self.config['generator']['update_interval'],
            self._generate_pattern
        )

        running_state = self.config['generator']['pattern_running']
        if running_state:
            pass


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
