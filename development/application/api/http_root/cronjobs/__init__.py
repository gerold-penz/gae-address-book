#!/usr/bin/env python
# coding: utf-8

import cherrypy
import common.http
import common.tag_items


@cherrypy.expose
def update_tag_items_cache():

    # Run job
    common.tag_items.update_tag_items_cache()

    # Finished
    common.http.set_content_type_text()
    return u"OK"

