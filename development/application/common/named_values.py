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

    if named_value is None:
        # Create new named value
        named_value = NamedValue()
        named_value.name = name

    # Edit value
    named_value.value = value

    # Save
    named_value.put()

    # Finished
    return named_value


def increment(name):
    """
    Increments the value with the given name, if it is an integer.
    """

    # Get existing named value
    named_value = get_value(name)

    if named_value is None:
        # Create new named value
        named_value = NamedValue()
        named_value.name = name
        named_value.value = 0

    # Edit value
    named_value.value += 1

    # Save
    named_value.put()

    # Finished
    return named_value


def decrement(name):
    """
    Decrements the value with the given name, if it is an integer.
    """

    # Get existing named value
    named_value = get_value(name)

    if named_value is None:
        # Create new named value
        named_value = NamedValue()
        named_value.name = name
        named_value.value = 1

    # Edit value
    named_value.value -= 1

    # Save
    named_value.put()

    # Finished
    return named_value
