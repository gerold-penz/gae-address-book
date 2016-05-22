#!/usr/bin/env python
# coding: utf-8

from model.named_value import NamedValue


def get_value(name):
    """
    Returns the value with the given name.
    """

    return NamedValue.query(NamedValue.name == name).get()


def set_value(name, value):
    """
    Sets the value with the given name.
    """

    # Get existing named value
    named_value = get_value(name)
    if not named_value:
        # Create new named value
        named_value = NamedValue()
        named_value.name = name
    named_value.value = value

    # Save
    named_value.put()

    # Finished
    return named_value
