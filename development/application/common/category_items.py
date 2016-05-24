#!/usr/bin/env python
# coding: utf-8

from model.address import Address
import named_values


CATEGORY_ITEMS = "category_items"


def get_category_items_direct():
    """
    Returns all used category items as set. Directly from the Address model.
    """

    category_items = set()

    query = Address.query(projection = [Address.category_items], distinct = True)
    for address in query.iter(batch_size = 200):

        for category_item in address.category_items:
            category_items.add(category_item)

    # Finished
    return category_items


def get_category_items_cached():
    """
    Returns all used category items as set.
    """

    # Cache get
    category_items = named_values.get_value(name = CATEGORY_ITEMS)
    if category_items is not None:
        return category_items

    # Fetch category items direct from the Address model
    category_items = get_category_items_direct()

    # Cache set
    named_values.set_value(name = CATEGORY_ITEMS, value = category_items)

    # Finished
    return category_items


def update_category_items_cache():
    """
    Updates the "category_items" NamedValue entity
    """

    # Cache set
    named_values.set_value(name = CATEGORY_ITEMS, value = get_category_items_direct())


def add_category_items_to_cache(category_items):
    """
    Add category items to the cache
    """

    if isinstance(category_items, basestring):
        category_items = [category_items]

    # Cache get
    cached_category_items = named_values.get_value(name = CATEGORY_ITEMS)
    if cached_category_items is None:
        cached_category_items = set()

    # Add new category items
    for category_item in category_items:
        cached_category_items.add(category_item)

    # Cache set
    named_values.set_value(name = CATEGORY_ITEMS, value = cached_category_items)


