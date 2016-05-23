#!/usr/bin/env python
# coding: utf-8

from model.address import Address
import named_values


BUSINESS_ITEMS = "business_items"


def get_business_items_direct():
    """
    Returns all used business items as set. Directly from the Address model.
    """

    business_items = set()

    query = Address.query(projection = [Address.business_items], distinct = True)
    for address in query.iter(batch_size = 200):
        for business_item in address.business_items:
            business_items.add(business_item)

    # Finished
    return business_items


def get_business_items_cached():
    """
    Returns all used business items as set.
    """

    # Cache get
    business_items = named_values.get_value(name = BUSINESS_ITEMS)
    if business_items is not None:
        return business_items

    # Fetch business items direct from the Address model
    business_items = get_business_items_direct()

    # Cache set
    named_values.set_value(name = BUSINESS_ITEMS, value = business_items)

    # Finished
    return business_items


def update_business_items_cache():
    """
    Updates the "business_items" NamedValue entity
    """

    # Cache set
    named_values.set_value(name = BUSINESS_ITEMS, value = get_business_items_direct())


def add_business_items_to_cache(business_items):
    """
    Add business items to the cache
    """

    if isinstance(business_items, basestring):
        business_items = [business_items]

    # Cache get
    cached_business_items = named_values.get_value(name = BUSINESS_ITEMS)

    # Add new business items
    for business_item in business_items:
        cached_business_items.add(business_item)

    # Cache set
    named_values.set_value(name = BUSINESS_ITEMS, value = cached_business_items)


