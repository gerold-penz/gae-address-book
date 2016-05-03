#!/usr/bin/env python
# coding: utf-8

import authorization
from google.appengine.ext import ndb
from model.free_defined_field import FreeDefinedField
from model.free_defined_field_history import FreeDefinedFieldHistory


def create(
    user,
    label,
    position = None,
):
    """
    Creates a new free defined field

    :param user: Username
    :param label: Label of the field
    :param position: sort key

    :return: New created and saved FreeDefinedField-Object

    :rtype: model.free_defined_field.FreeDefinedField
    """

    # Check authorization
    authorization.check_authorization(user, authorization.FREE_DEFINED_FIELD_CREATE)

    # Create field
    free_defined_field = FreeDefinedField(
        cu = user,
        label = label,
        position = position
    )

    # Save
    free_defined_field.put()

    # Finished
    return free_defined_field


def get_free_defined_fields():
    """
    Returns a list with free defined field objects
    """

    # Query
    query = FreeDefinedField.query()

    # Sorting
    query = query.order(FreeDefinedField.position, FreeDefinedField.label)

    # Fetch adresses
    free_defined_fields = []
    for free_defined_field in query:
        free_defined_fields.append(free_defined_field)

    # Finished
    return free_defined_fields


def get_free_defined_field(key_urlsafe):
    """
    Returns one free_defined_field
    """

    key = ndb.Key(urlsafe = key_urlsafe)
    return key.get()


def save_free_defined_field(
    user,
    key_urlsafe = None,
    label = None,
    position = None
):
    """
    Saves one free_defined_field

    :param user: Username
    :param key_urlsafe: Key
    :param label: Label
    :param position: Sort key

    :return: Edited FreeDefinedField-Object

    :rtype: model.free_defined_field.FreeDefinedField
    """

    # Load original free defined field
    free_defined_field = get_free_defined_field(key_urlsafe = key_urlsafe)

    # Check authorization
    authorization.check_authorization(user, authorization.FREE_DEFINED_FIELD_EDIT)

    # Save original field to *free_defined_field_history*.
    free_defined_field_history = FreeDefinedFieldHistory(
        cu = user,
        free_defined_field_key = free_defined_field.key,
        free_defined_field_dict = free_defined_field.to_dict()
    )
    free_defined_field_history.put()

    # Check arguments and set values
    if label is not None:
        free_defined_field.label = label
    if position is not None:
        free_defined_field.position = position

    # save changes
    free_defined_field.put()

    # Return saved field
    return free_defined_field


def delete_free_defined_field(key_urlsafe = None):
    """
    Deletes one free defined field
    """

    # Delete free defined field
    key = ndb.Key(urlsafe = key_urlsafe)
    key.delete()

