#!/usr/bin/env python2
# coding=utf-8

"""Wrapper for User Input."""

import sys
import traceback


def pre_handler(user_input, handle_userinput=None):
    """Pre-handler."""
    flag_run = True
    try:
        if len(user_input) > 0:
            if handle_userinput:
                flag_run = handle_userinput(user_input)
            else:
                flag_run = False
    except Exception as e:
        print("unknown error: {}".format(e))
        traceback.print_exc()
        flag_run = False
        print("stop script.")
    return flag_run


def request_userinput(message, handle_userinput=None):
    """Request userinput."""
    flag_run = True
    # handle different python versions:
    try:
        if sys.version_info.major >= 3:
            # python3
            user_input = input(message)
        elif sys.version_info.major == 2:
            # python2
            user_input = raw_input(message)
        else:
            # no input methode found.
            user_input = "q"
    except KeyboardInterrupt:
        print("\nstop script.")
        flag_run = False
    except EOFError:
        print("\nstop script.")
        flag_run = False
    except Exception as e:
        print("unknown error: {}".format(e))
        flag_run = False
        print("stop script.")
    else:
        flag_run = pre_handler(user_input, handle_userinput)
    return flag_run
