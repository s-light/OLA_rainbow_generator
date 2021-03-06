#!/usr/bin/env python2
# coding=utf-8

"""
Rainbow.

Create a nice rainbow pattern.
"""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


import sys
import os
import json
import time
# import signal
import argparse

from modules.configdict import ConfigDict
# from modules.userinput import request_userinput
from modules.readline_history import setup_readline_history

from modules.rainbow_generator import RainbowGenerator
from interface_interactive import InterfaceInteractive
from interface_web import InterfaceWeb

# classes

# class RGB(object):
#     """Holds one RGB value."""
#
#     def __init__(self, red=0, green=0, blue=0):
#         """Initialize with optional values."""
#         super(RGB, self).__init__()
#         self.red = red
#         self.green = green
#         self.blue = blue


class MainHandler(object):
    """
    OLA Rainbow Generator.

    this script can generate rainbows and output them to ola.
    goal is to have an additional webinterface for controlling
    dimming and pattern speed.
    """

    config_defaults = {
        'generator': {},
        'webinterface': {},
    }

    path_script = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        """Init main Application Class."""
        # super(OLAThread, self).__init__()
        object.__init__(self)

        self.init_cmdline()
        self.verbose = self.args.verbose

        # init flag_run
        self.flag_run = False

        # setup termination and interrupt handling:
        # signal.signal(signal.SIGINT, self._exit_helper)
        # signal.signal(signal.SIGTERM, self._exit_helper)

        self.read_config()

        self.rainbow_generator = RainbowGenerator(self.config, self.verbose)

        setup_readline_history()
        self.interface_interactive = InterfaceInteractive(
            self.config,
            self.verbose,
            self
        )
        self.interface_web = InterfaceWeb(
            self.config,
            self.verbose,
            self
        )

        if self.verbose:
            print("MainHandler config: {}".format(
                json.dumps(
                    self.config,
                    sort_keys=True,
                    indent=4,
                    separators=(',', ': ')
                )
            ))
            print("--> init finished.")
            # print("config: {}".format(self.config))

    def read_config(self, filename=None):
        """Read and parse configuration."""
        if not filename:
            if "config" in self.args:
                filename = self.args.config
            else:
                filename = self.filename_default
        # check for filename
        if not os.path.exists(filename):
            # print(
            #     "filename does not exists.. "
            #     "so we creating a hopefully valid path"
            # )
            # remember config file name
            config_name = os.path.basename(filename)
            # create path on base of script dir.
            # path_to_config = os.path.join(self.path_script, "config")
            path_to_config = self.path_script
            filename = os.path.join(path_to_config, config_name)

        # read config file:
        self.my_config = ConfigDict(self.config_defaults, filename)
        # print("my_config.config: {}".format(self.my_config.config))
        self.config = self.my_config.config
        # print("config: {}".format(self.config))

        # generate absolute path to config files
        path_to_config = os.path.dirname(filename)
        self.config["path_to_config"] = path_to_config

    def init_cmdline(self):
        """Init commandline arguments handling."""
        self.filename_default = "./config.json"

        parser = argparse.ArgumentParser(
            description="generate rainbow - output with olad"
        )
        parser.add_argument(
            "-c",
            "--config",
            help="specify a location for the config file (defaults to {})".
            format(
                self.filename_default
            ),
            metavar='FILENAME',
            default=self.filename_default
        )
        parser.add_argument(
            "-s",
            "--saveconfig",
            help="save config on exit",
            action="store_true"
        )
        parser.add_argument(
            "-i",
            "--interactive",
            help="run in interactive mode",
            action="store_true"
        )
        parser.add_argument(
            "-v",
            "--verbose",
            help="show advanced log information"
            "(specify multiple times for more details)",
            action="count"
        )
        self.args = parser.parse_args()

    def _exit_helper(self, signal, frame):
        """Stop loop."""
        self.flag_run = False

    ##########################################

    def not_interactive_waiting(self):
        """Run application."""
        # wait for user to hit key.
        # request_userinput("hit Enter-Key or Ctrl+C to stop this..")
        # this could be exchanged with an while loop just sleeping.
        while self.flag_run:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                self.flag_run = False

    def run(self):
        """Run application."""
        self.flag_run = True
        self.rainbow_generator.start_ola()
        self.interface_web.start()

        if self.args.interactive:
            self.interface_interactive.run()
            self.flag_run = False
        else:
            self.not_interactive_waiting()
            self.flag_run = False
        print("\nstop.")

        # blocks untill thread has joined.
        self.rainbow_generator.stop_ola()
        self.interface_web.stop()

        if "saveconfig" in self.args:
            if self.args.saveconfig:
                self.my_config.write_to_file()
                print("saved configutaion.")


##########################################
if __name__ == '__main__':

    print(42 * '*')
    print("Python Version: " + sys.version)
    print(42 * '*')

    global main_handler
    main_handler = MainHandler()
    main_handler.run()

##########################################
