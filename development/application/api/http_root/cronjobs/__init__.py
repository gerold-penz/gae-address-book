#!/usr/bin/env python
# coding: utf-8

import os
import logging
import cherrypy
import datetime
import common.constants
import common.http
import common.tag_items
import common.category_items
import common.business_items
import common.addresses
from google.appengine.api import taskqueue
try:
    from google.appengine.api import app_identity
except ImportError:
    app_identity = None


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


@cherrypy.expose
def backup_database():
    """
    Passt den Zielpfad an und erstellt einen Task der das Backup ausführt.
    """

    # Google Cloud Storage
    bucket_name = os.environ.get(
        "BUCKET_NAME",
        app_identity.get_default_gcs_bucket_name() if app_identity else None
    )

    # Parameter anpassen
    iso_date = datetime.date.today().isoformat()
    iso_year = iso_date[0:4]
    iso_month = iso_date[5:7]
    iso_day = iso_date[8:10]
    params = dict(
        name = "DatabaseBackup",
        kind = [
            "Address",
            "AddressHistory",
            "FreeDefinedField",
            "NamedValue",
            "DeletedAddress",
        ],
        filesystem = "gs",
        gs_bucket_name = "{bucket_name}/backups/{iso_year}/{iso_month}/{iso_day}".format(
            bucket_name = bucket_name,
            iso_year = iso_year,
            iso_month = iso_month,
            iso_day = iso_day
        )
    )

    # Job erstellen
    taskqueue.add(
        url = "/_ah/datastore_admin/backup.create",
        params = params,
        target = "ah-builtin-python-bundle"
    )










