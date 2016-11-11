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


def _do_iteration():

    index = 0

    for address in Address.query(Address.tag_items == u"Imabis-Import"):
        assert isinstance(address, Address)

        # Log
        index += 1
        if index % 100 == 0:
            logging.info("do_iteration: {index}".format(index = index))

        # Erste E-Mail-Adresse ermitteln
        if address.email_items:
            email = address.email_items[0].email

            deferred.defer(
                _do_iteration_part2,
                email = email,
                _queue = "onebyone"
            )


    logging.info("Do-Iteration fertig")

    return True


def _do_iteration_part2(email):

    # E-Mail in Excel-Import suchen
    result = common.addresses.get_addresses_by_search(
        page = 1,
        page_size = 100,
        query_string = u'tag = "Excel-Import" AND email = "{email}"'.format(email = email),
    )
    for excel_address in result["addresses"]:
        # Excel-Adresse löschen
        logging.info("Adresse wird geloescht PROD")
        common.addresses.delete_address(
            user = "gerold",
            key_urlsafe = excel_address.key.urlsafe(),
            force = True
        )






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
