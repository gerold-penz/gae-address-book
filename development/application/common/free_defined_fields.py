#!/usr/bin/env python
# coding: utf-8

import authorization
from google.appengine.ext import ndb
from model.free_defined_field import FreeDefinedField


def create(
    user,
    group,
    label,
    position = None,
    visible = None
):
    """
    Creates a new free defined field

    :param group: Group name
    :param user: Username
    :param label: Label of the field
    :param position: Sort key
    :param visible: Visibility of the field

    :return: New created and saved FreeDefinedField-Object

    :rtype: model.free_defined_field.FreeDefinedField
    """

    # Check authorization
    authorization.check_authorization(user, authorization.FREE_DEFINED_FIELD_CREATE)

    # Create field
    free_defined_field = FreeDefinedField(
        cu = user,
        group = group,
        label = label,
        position = position,
        visible = visible
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
    group = None,
    label = None,
    position = None,
    visible = None
):
    """
    Saves one free_defined_field

    :param user: Username
    :param key_urlsafe: Key
    :param group: Group name
    :param label: Label
    :param position: Sort key
    :param visible: Visibility of the field

    :return: Edited FreeDefinedField-Object

    :rtype: model.free_defined_field.FreeDefinedField
    """

    # Load original free defined field
    free_defined_field = get_free_defined_field(key_urlsafe = key_urlsafe)

    # Check authorization
    authorization.check_authorization(user, authorization.FREE_DEFINED_FIELD_EDIT)

    # Check arguments and set values
    if group is not None:
        free_defined_field.group = group
    if label is not None:
        free_defined_field.label = label
    if position is not None:
        free_defined_field.position = position
    if visible is not None:
        free_defined_field.visible = visible

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

