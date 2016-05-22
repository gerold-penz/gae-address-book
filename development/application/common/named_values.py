#!/usr/bin/env python
# coding: utf-8

from model.named_value import NamedValue

_global_keys = {}


def get_value(name):
    """
    Returns the value with the given name.
    """

    try:
        return _global_keys[name].get()
    except KeyError:
        named_value = NamedValue.query(NamedValue.name == name).get()
        _global_keys[name] = named_value.key
        return named_value


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

    # Edit value
    named_value.value = value

    # Save
    named_value.put()

    # Finished
    return named_value
