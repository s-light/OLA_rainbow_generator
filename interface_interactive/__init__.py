#!/usr/bin/env python
# coding=utf-8

"""The Interactive commandline interface."""

from __future__ import print_function
# https://docs.python.org/2.7/howto/pyporting.html#division
from __future__ import division

import traceback

import modules.configdict as configdict
from modules.userinput import request_userinput
# from modules.readline_history import setup_readline_history
# from modules.exception_classes import FormatError


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

        self.init_menu_entries_longest_lengths()

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
            try:
                self.flag_run = request_userinput(
                    self.generate_menu_message(),
                    self.handle_userinput
                )
            except Exception:
                self.flag_run = False
                traceback.print_exc()

    def generate_menu_message(self):
        """Genrate menu messagae."""
        message = ""
        message += 42 * "*" + "\n"
        message += self.parent.__doc__ + "\n"
        message += 42 * "*" + "\n"
        for entry_name in self.menu_entry_order:
            if entry_name in self.menu_entries:
                entry = self.menu_entries[entry_name]
                message += self.generate_message_for_entry(entry_name, entry)
        message += 42 * "*" + "\n"
        return message

    def handle_userinput(self, user_input):
        """Handle userinput."""
        # print("handle_userinput")
        flag_run = True
        # print("user_input: ", user_input)
        entry_name, menu_entry = self.find_entry_from_shortcode(user_input)
        # print("entry_name: {} menu_entry: {}".format(entry_name, menu_entry))
        if menu_entry:
            # print(" --> handle_entry_userinput")
            flag_run = self.handle_entry_userinput(user_input, menu_entry)
        else:
            print("unrecorgnized value. try again.")
        return flag_run

    ##########################################
    # menu messagae creation

    def init_menu_entries_longest_lengths(self):
        """Run Once through names of menu entries and find longest name."""
        # print("find longest menu entry name..")
        longest_name_length = 0
        longest_shortcode_length = 0
        for name, entry in self.menu_entries.items():
            if len(name) > longest_name_length:
                longest_name_length = len(name)
            if "shortcode" in entry:
                if len(entry['shortcode']) > longest_shortcode_length:
                    longest_shortcode_length = len(entry['shortcode'])
        # print("found: {}".format(longest_shortcode_length))
        self._menu_entries_longest_name_length = longest_name_length
        self._menu_entries_longest_shortcode_length = longest_shortcode_length

    def generate_message_for_entry(self, entry_name, menu_entry):
        """Handle userinput."""
        message = ""
        # check if we generate a messagae at all..
        if (("shortcode" in menu_entry) and ("info" in menu_entry)):
            # this is the final generated string:
            # "  'ui' update_interval --> set update interval (50ms)"
            # "  '{shortcode}' {name} --> {info} "
            # "({parameter_value}{parameter_unit})"
            #
            # setup possible parts
            format_string = ""
            format_parameter = ""
            parameter_value = None
            parameter_unit = ""
            info_extra = ""
            # *********************
            # fill format_string & values with content
            format_string += (
                "  '{shortcode:<" +
                "{}".format(self._menu_entries_longest_shortcode_length) +
                "}' "
                "{name:<" +
                "{}".format(self._menu_entries_longest_name_length) +
                "} "
                "--> {info}"
            )
            if "parameter" in menu_entry:
                format_parameter += "{parameter_value}"
                parameter_value = self.walk_parameter_and_get_or_set(
                    menu_entry["parameter"],
                    self
                )
            if "parameter_unit" in menu_entry:
                format_parameter += "{parameter_unit}"
                parameter_unit = menu_entry["parameter_unit"]
            if format_parameter:
                format_string += " (" + format_parameter + ")"
            if "info_extra" in menu_entry:
                # format_string += " {info_extra}"
                # info_extra = menu_entry["info_extra"]
                # TODO: implement info_extra text thing
                pass
            # render message
            message = format_string.format(
                name=entry_name,
                shortcode=menu_entry["shortcode"],
                info=menu_entry["info"],
                parameter_value=parameter_value,
                parameter_unit=parameter_unit,
                info_extra=info_extra
            )
        message += "\n"
        return message

    ##########################################
    # menu input handling

    def find_entry_from_shortcode(self, user_input):
        """Find menu item for user_input."""
        entry_name = None
        entry_config = None
        for name, entry in self.menu_entries.items():
            if "shortcode" in entry:
                if user_input.startswith(entry["shortcode"]):
                    entry_name = name
                    entry_config = entry
        return (entry_name, entry_config)

    def handle_entry_userinput(self, user_input, menu_entry):
        """Take aktion acording to entry."""
        flag_run = True
        if "parser_type" in menu_entry:
            # parse value regarding choosen parser
            self.handle_input_for_entry(user_input, menu_entry)
        elif "callback_func" in menu_entry:
            flag_run = self.callback_func_for_entry(user_input, menu_entry)
        else:
            # nothing to do.
            pass
        return flag_run

    def handle_input_for_entry(self, user_input, menu_entry):
        """Parser input with parser_type from entry."""
        parser_type = menu_entry["parser_type"]
        parser_function = None
        if parser_type in self.parser_types:
            parser_function = self.parser_types[parser_type]
            if parser_function:
                raw_value = parser_function(user_input)
                if raw_value:
                    value = self.check_input(raw_value, menu_entry)
                    if value:
                        self.menu_entry_set_parameter(value, menu_entry)

    def callback_func_for_entry(self, user_input, menu_entry):
        """Callback Function for entry."""
        flag_run = True
        callback_func = menu_entry["callback_func"]
        if callback_func:
            flag_run = callback_func(user_input)
        return flag_run

    def check_input_message(self, name, message, message_value):
        """Print Check messagae."""
        if self.verbose and message:
            if message_value:
                # means it is restricted
                print(
                    "'{name}' parameter restricted to {restriction} value"
                    " ({value})".format(
                        name=name,
                        restriction=message,
                        value=message_value
                    )
                )
            else:
                # fails
                print(
                    "'{name}' parameter check failed. "
                    "{restriction} bound hit.".format(
                        name=name,
                        restriction=message,
                        value=message_value
                    )
                )

    def check_input(self, value, menu_entry):
        """Check if new input falls within defined bounds from entry."""
        # "bounds": {
        #     "min": 0,
        #     "max": 10000,
        # },
        result_value = value
        if "bounds" in menu_entry:
            bounds = menu_entry["bounds"]
            if "mode" in bounds:
                restrict_flag = False
                if bounds["mode"] is "restrict":
                    restrict_flag = True
            message = ""
            message_value = None
            if "min" in bounds:
                if value <= bounds["min"]:
                    message = "minimum"
                    if restrict_flag:
                        result_value = bounds["min"]
                        message_value = bounds["min"]
                    else:
                        result_value = None
            if "max" in bounds:
                if value <= bounds["max"]:
                    message = "maximum"
                    if restrict_flag:
                        result_value = bounds["max"]
                        message_value = bounds["max"]
                    else:
                        result_value = None
            self.check_input_message(
                menu_entry["name"],
                message,
                message_value
            )
        return result_value

    def walk_parameter_and_get_or_set(
        self,
        param_string,
        reference,
        value=None
    ):
        """
        Walk parameter string and set.

        Walk the parameter dot notation string
        until last part (no more dots) is found.
        then set value if value is given.
        otherwise gets value and returns this.
        """
        # "parameter": "parent.rainbow_generator.update_interval",
        # function calls itself if a nother level of dot notation is found.
        result = None
        if '.' not in param_string:
            if value:
                setattr(reference, param_string, value)
            else:
                result = getattr(reference, param_string)
        else:
            current_name, sub_string = param_string.split('.', 1)
            sub_ref = getattr(reference, current_name)
            result = self.walk_parameter_and_get_or_set(
                sub_string,
                sub_ref,
                value
            )
        return result

    def menu_entry_set_parameter(self, value, menu_entry):
        """Set Parameter from menu entry with new value."""
        # "parameter": "parent.rainbow_generator.update_interval",
        if "parameter" in self.parser_types:
            param_string = self.parser_types.parameter
            self.walk_parameter_and_set(param_string, self, value)

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

    parser_types = {
        "int": parse_ui__integer,
        # "float": parse_ui__float,
        # "bool": parse_ui__bool,
    }

    ##########################################
    # special menu callback functions

    def menu_entry_cbf__quit(self, user_input):
        """Parse quit."""
        self.flag_run = False

    def menu_entry_cbf__save_config(self, user_input):
        """Parse save_config."""
        # save config to file
        print("write config.")
        self.parent.my_config.write_to_file()

    ##########################################
    # menu config

    #  example entry
    # the descriptiv name of the entry
    # "update_interval": {
    #     entry chooser shortcode
    #     "shortcode":"ui",
    #     a description
    #     "info": "set update interval",
    #     the parameter on self that should be set (dot notation)
    #     "parameter": "parent.rainbow_generator.update_interval",
    #     "parameter_unit": "ms",
    #     format parser
    #     "parser_type": "int",
    #     bound information for value
    #     "bounds": {
    #         "mode": "restrict | fail"
    #         "min": 0,
    #         "max": 10000,
    #     },
    # },

    menu_entries = {
        "update_interval": {
            "shortcode": "ui",
            "info": "set update interval",
            # "info_extra": " ({update_frequency}Hz)",
            "parameter": "parent.rainbow_generator.update_interval",
            "parameter_unit": "ms",
            "parser_type": "int",
            "bounds": {
                "mode": "fail",
                "min": 0,
                "max": 10000,
            },
        },
        "universe": {
            "shortcode": "uo",
            "info": "set universe",
            "parameter": "parent.rainbow_generator.universe",
            "parser_type": "int",
            "bounds": {
                "mode": "fail",
                "min": 1,
                "max": 4000,
            },
        },
        "pattern_duration": {
            "shortcode": "pd",
            "info": "set pattern duration",
            "parameter": "parent.rainbow_generator.pattern_duration",
            "parameter_unit": "s",
            "parser_type": "int",
            "bounds": {
                "mode": "restrict",
                "min": 1,
                "max": 10000,
            },
        },
        "brightness": {
            "shortcode": "b",
            "info": "set brightness",
            "parameter": "parent.rainbow_generator.brightness",
            "parser_type": "int",
            "bounds": {
                "mode": "restrict",
                "min": 0,
                "max": 255,
            },
        },
        "quit": {
            "shortcode": "q",
            "info": "Ctrl+C or 'q' to stop script",
            "callback_func": menu_entry_cbf__quit,
        },
        "save_config": {
            "shortcode": "sc",
            "info": "save config",
            "callback_func": menu_entry_cbf__save_config,
        },
        "-": {
            "info": "",
        },
    }

    menu_entry_order = [
        "update_interval",
        "universe",
        "-",
        "pattern_duration",
        "brightness",
        "-",
        "quit",
        "save_config",
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
