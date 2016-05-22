#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb
from model.address import Address
import named_values


TAG_ITEMS = "tag_items"


def get_tag_items_direct():
    """
    Returns all uses tag items as set. Directly from the Address model.
    """


    tag_items = set()

    query = Address.query(projection = [Address.tag_items], distinct = True)
    for address in query.iter(batch_size = 200):
        for tag_item in address.tag_items:
            tag_items.add(tag_item)

    # Finished
    return tag_items


def get_tag_items_cached():
    """
    Returns all used tag items as set.
    """

    # Cache get
    tag_items = named_values.get_value(name = TAG_ITEMS)
    if tag_items is not None:
        return tag_items

    # Fetch tag items direct from the Address model
    tag_items = get_tag_items_direct()

    # Cache set
    named_values.set_value(name = TAG_ITEMS, value = tag_items)

    # Finished
    return tag_items


def update_tag_items_cache():
    """
    Updates the "tag_items" NamedValue entity
    """

    # Cache set
    named_values.set_value(name = TAG_ITEMS, value = get_tag_items_direct())


def add_tag_items_to_cache(tag_items):
    """
    Add tag items to the cache
    """

    if isinstance(tag_items, basestring):
        tag_items = [tag_items]

    # Cache get
    cached_tag_items = named_values.get_value(name = TAG_ITEMS)

    # Add new tag items
    for tag_item in tag_items:
        cached_tag_items.add(tag_item)

    # Cache set
    named_values.set_value(name = TAG_ITEMS, value = cached_tag_items)


