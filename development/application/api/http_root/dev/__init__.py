#!/usr/bin/env python
# coding: utf-8

import os
import logging
import cherrypy
import hashlib
import threading
import common.addresses
from pyjsonrpc.cp import CherryPyJsonRpc, rpcmethod
from google.appengine.ext import deferred
from google.appengine.api import search
from common.model.address import (
    Address
)


THISDIR = os.path.dirname(os.path.abspath(__file__))


# Globale Variable um die Benutzer (threadübergreifend) zwischenzuspeichern
_users = None
_users_lock = threading.Lock()


def _security_users():
    """
    Returns the dev.users (security.ini)
    """

    global _users

    if _users:
        return _users

    with _users_lock:
        _users = {}
        for key, value in cherrypy.config["dev.users"].items():
            _users[key] = hashlib.md5(value).hexdigest()

    return _users


class JsonRpc(CherryPyJsonRpc):
    """
    Dev-Api-Zugang
    """

    _cp_config = {
        "tools.basic_auth.on": True,
        "tools.basic_auth.realm": "Dev API Zugang",
        "tools.basic_auth.users": _security_users
    }

    index = CherryPyJsonRpc.request_handler


    @rpcmethod
    def start_iteration(self):

        # Hilfsfunktion per Deferred aufrufen
        deferred.defer(
            _do_iteration,
            _queue = "onebyone"
        )

        return True


# Json-Rpc-Schnittstelle aktivieren
jsonrpc = JsonRpc()
jsonrpc.exposed = True




# ---------------------------------




def _do_iteration():

    index = search.Index("Address")
    cursor = search.Cursor()
    iternumber = 0

    
    # Domains und doc_ids sammeln
    while cursor:

        iternumber += 1
        logging.info("Iteration: {iternumber}".format(iternumber = iternumber))

        options = search.QueryOptions(limit = 100, cursor = cursor, ids_only = True)

        query_string = " OR ".join([
            'email = "{email}"'.format(email = email) for email in [
                "thomas.wurzer@immoads.at",
                "max.muster@immoads.at"
            ]
        ])
        assert len(query_string) < 2000


        query = search.Query(
            query_string = query_string,
            options = options
        )

        results = index.search(query)
        cursor = results.cursor

        for i, document in enumerate(results):
            doc_id = document.doc_id
            deferred.defer(
                _do_iteration_part2,
                doc_id = doc_id,
                _queue = "noretry"
            )

    logging.info("Do-Iteration fertig")

    return True


def _do_iteration_part2(doc_id):

    print u"DoIt....", doc_id

    address = common.addresses.get_address(key_urlsafe = doc_id)
    tag_items = address.tag_items or []
    tag_items.append("XXX")

    common.addresses.save_address(
        user = "gerold",
        key_urlsafe = doc_id,
        tag_items = tag_items

    )


    # common.addresses.delete_address(
    #     user = "gerold",
    #     key_urlsafe = doc_id,
    #     force = True
    # )





# # Nur geänderte Daten speichern
# changed = False
#
#
# if not address.category_items:
#     address.category_items = []
# address.category_items.append(u"Kunde-nein")
# address.category_items.remove(u"Kunde nein")
# changed = True
#
#
# # if address.category_items and u"Immoads" in (address.category_items or []):
# #     address.category_items.append(u"Makler")
# #     address.category_items.remove(u"Immoads")
# #     changed = True
# #
# # if address.tag_items and u"Kunde nein" in (address.tag_items or []):
# #     if not address.category_items:
# #         address.category_items = []
# #     address.category_items.append(u"Kunde nein")
# #     address.tag_items.remove(u"Kunde nein")
# #     changed = True
# #
# # if address.tag_items and u"Imabis 2016-11" in (address.tag_items or []):
# #     address.tag_items.remove(u"Imabis 2016-11")
# #     changed = True
#
# # Speichern
# if changed:
#     address.put()
