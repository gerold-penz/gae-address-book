#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb
from model.address import Address


def get_tag_items():
    """
    Returns all used tag items as set.
    """

    tag_items = set()

    query = Address.query(projection = [Address.tag_items], distinct = True)
    for address in query.iter(batch_size = 1000):
        for tag_item in address.tag_items:
            tag_items.add(tag_item)

    # Finished
    return tag_items
