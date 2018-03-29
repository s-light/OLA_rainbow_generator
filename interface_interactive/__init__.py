#!/usr/bin/env python
# coding=utf-8

"""The Interactive commandline interface."""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division


import modules.configdict as configdict
from modules.userinput import request_userinput
# from modules.readline_history import setup_readline_history
from modules.exception_classes import FormatError


class InterfaceInteractive(object):
    """Interactive commandline interface."""

    config_defaults = {
        'interface_interactive': {

        },
    }

    def __init__(self, config, verbose=False, parent=None):
        """Init main Application Class."""
        # super(OLAThread, self).__init__()
        object.__init__(self)
        self.verbose = verbose

        # extend config with defaults
        self.config = config
        configdict.extend_deep(self.config, self.config_defaults.copy())

        self.parent = parent

        # init flag_run
        self.flag_run = False

        # setup termination and interrupt handling:
        # signal.signal(signal.SIGINT, self._exit_helper)
        # signal.signal(signal.SIGTERM, self._exit_helper)

    ##########################################

    def run(self):
        """Handle interactive."""
        print(
            (42 * '*') + "\n" +
            __doc__ + "\n" +
            (42 * '*') + "\n"
        )
        self.flag_run = True
        while self.flag_run:
            message = (
                "interactive mode.\n"
                "not implemented yet.. \n"
                "hit 'Ctrl + C' or 'q + Enter' to stop this..\n"
            )
            self.flag_run = request_userinput(message, self.handle_userinput)

    def handle_userinput(self, user_input):
        """Handle userinput."""
        flag_run = True
        menu_key, menu_entry = self.find_menu_entry(user_input)
        if menu_entry:
            flag_run = self.handle_entry_userinput(user_input, menu_entry)
        else:
            print("unrecorgnized value. try again.")
        return flag_run

    ##########################################
    # menu handling

    def find_menu_entry(self, user_input):
        """Find menu item for user_input."""
        menu_key = None
        menu_item = None
        for key, value in self.menu_entries.items():
            if user_input.startswith(key):
                menu_key = key
                menu_item = value
        return (menu_key, menu_item)

    def handle_entry_userinput(self, user_input, menu_entry):
        """Take aktion acording to entry."""
        flag_run = True
        if "parser_type" in menu_entry:
            # parse value regarding choosen parser
            flag_run = self.parse_input_for_entry(user_input, menu_entry)
        elif "callback_func" in menu_entry:
            flag_run = self.callback_func_for_entry(user_input, menu_entry)
        else:
            # nothing to do.
            pass
        return flag_run

    def parse_input_for_entry(self, user_input, menu_entry):
        """Get the parser funciton from the user_input."""
        pass

    ##########################################
    # parser

    def parse_ui__integer(self, user_input):
        """Parse update interval."""
        result = None
        start_index = user_input.find(':')
        if start_index > -1:
            value_new = user_input[start_index + 1:]
            try:
                value_new = int(value_new)
            except Exception as e:
                print("input not a valid Integer. ({})".format(e))
            else:
                result = value_new
        return result

    def parse_ui__quit(self, user_input):
        """Parse quit."""
        self.flag_run = False

    def parse_ui__save_config(self, user_input):
        """Parse save_config."""
        # save config to file
        print("\nwrite config.")
        self.parent.my_config.write_to_file()

    parser_type = {
        "int": parse_ui__integer,
        # "float": parse_ui__float,
        # "bool": parse_ui__bool,
    }

    ##########################################
    # menu config

    menu_entries = {
        "ui": {
            "info": "update interval",
            # "example": "{parameter} ({update_frequency}Hz)",
            # "example": "{parameter}",
            "parameter": "parent.rainbow_generator.update_interval",
            "parser_type": "int",
            "value": {
                "min": 0,
                "max": 10000,
            },
        },
        "uo": {
            "info": "set universe output",
            "parser_type": "int",
            "value": {
                "min": 1,
                "max": 4000,
            },
        },
        "pd": {
            "info": "pattern duration",
            "parser_type": "int",
            "value": {
                "min": 1,
                "max": 10000,
            },
        },
        "b": {
            "info": "set brightness",
            "parser_type": "int",
            "value": {
                "min": 0,
                "max": 255,
            },
        },
        "q": {
            "info": "Ctrl+C or 'q' to stop script",
            "callback_func": parse_ui__quit,
        },
        "sc": {
            "info": "save config",
            "callback_func": parse_ui__save_config,
        },
        "-": {
            "info": "",
        },
    }

    parser_functions_order = [
        "-",
        "ui",
        "-",
        "sc",
        "q",
    ]

    ##########################################


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
