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
    Address, AnniversaryItem
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
    def replace_anmeldung_kunde_seit(self):

        # Hilfsfunktion per Deferred aufrufen
        deferred.defer(_replace_anmeldung_kunde_seit)

        return True


# Json-Rpc-Schnittstelle aktivieren
jsonrpc = JsonRpc()
jsonrpc.exposed = True


def _replace_anmeldung_kunde_seit():

    for address in Address.query():
        assert isinstance(address, Address)
        # logging.info(repr(address.organization))

        saved = True
        for anniversary_item in address.anniversary_items:
            assert isinstance(anniversary_item, AnniversaryItem)
            if anniversary_item.label == u"Anmeldung":
                anniversary_item.label = u"Kunde seit"
                saved = False

        if not saved:
            address.put()

    logging.info("Fertig")

    return True
