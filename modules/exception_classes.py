#!/usr/bin/python3
# coding=utf-8

"""User Defined Exceptions."""

# inspired by
# https://docs.python.org/3/tutorial/errors.html#tut-userexceptions


class FormatError(Exception):
    """Exception raised for errors in the format of the input.

    Attributes:
        expected_format -- description / example of the expected format
        message -- explanation of the error
        value -- input value in which the error occurred
    """

    def __init__(self, expected_format, message, value):
        """Init."""
        self.expected_format = expected_format
        self.message = message
        self.value = value

    def __str__(self):
        """String representation."""
        result = (
            # "message:{message} expected:{expected} got:{value}"
            "FormatError:\n"
            "    message:{message}\n"
            "    expected:{expected}\n"
            "    got:{value}"
        ).format(
            message=self.message,
            expected=self.expected_format,
            value=repr(self.value)
        )
        return result

    def __repr__(self):
        """String representation."""
        result = (
            "message:{message} expected:{expected} got:{value}"
        ).format(
            message=self.message,
            expected=self.expected_format,
            value=repr(self.value)
        )
        return result
