#!/usr/bin/env python
# coding: utf-8

import os
import logging
import cherrypy
import hashlib
import threading
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
        deferred.defer(_do_iteration)

        return True


# Json-Rpc-Schnittstelle aktivieren
jsonrpc = JsonRpc()
jsonrpc.exposed = True


def _do_iteration():

    # index = 0
    #
    # for address in Address.query(Address.tag_items == u"Gelöscht"):
    #     assert isinstance(address, Address)
    #
    #     # Log
    #     index += 1
    #     if index % 100 == 0:
    #         logging.info("do_iteration: {index}".format(index = index))
    #
    #     # Nur geänderte Daten speichern
    #     changed = False
    #
    #
    #     if not address.category_items:
    #         address.category_items = []
    #     address.category_items.append(u"Kunde inaktiv")
    #     address.tag_items.remove(u"Gelöscht")
    #     changed = True
    #
    #
    #     # if address.category_items and u"Immoads" in (address.category_items or []):
    #     #     address.category_items.append(u"Makler")
    #     #     address.category_items.remove(u"Immoads")
    #     #     changed = True
    #     #
    #     # if address.tag_items and u"Kunde nein" in (address.tag_items or []):
    #     #     if not address.category_items:
    #     #         address.category_items = []
    #     #     address.category_items.append(u"Kunde nein")
    #     #     address.tag_items.remove(u"Kunde nein")
    #     #     changed = True
    #     #
    #     # if address.tag_items and u"Imabis 2016-11" in (address.tag_items or []):
    #     #     address.tag_items.remove(u"Imabis 2016-11")
    #     #     changed = True
    #
    #     # Speichern
    #     if changed:
    #         address.put()

    logging.info("Fertig")

    return True
