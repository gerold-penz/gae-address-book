#!/usr/bin/env python
# coding: utf-8

import cherrypy
import common.http
import common.tag_items
import common.category_items
import common.business_items
import common.addresses


@cherrypy.expose
def update_tag_items_cache():

    # Run job
    common.tag_items.update_tag_items_cache()

    # Finished
    common.http.set_content_type_text()
    return u"OK"



@cherrypy.expose
def update_category_items_cache():

    # Run job
    common.category_items.update_category_items_cache()

    # Finished
    common.http.set_content_type_text()
    return u"OK"


@cherrypy.expose
def update_business_items_cache():

    # Run job
    common.business_items.update_business_items_cache()

    # Finished
    common.http.set_content_type_text()
    return u"OK"


@cherrypy.expose
def update_address_quantity_cache():

    # Run job
    common.addresses.update_address_quantity_cache()

    # Finished
    common.http.set_content_type_text()
    return u"OK"


@cherrypy.expose
def update_address_search_index():

    # Run job
    common.addresses.update_address_search_index()

    # Finished
    common.http.set_content_type_text()
    return u"OK"

