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
    addresses = {}
    
    
    # Domains und doc_ids sammeln
    while cursor:
        iternumber += 1
        logging.info("Iteration: {iternumber}".format(iternumber = iternumber))

        options = search.QueryOptions(limit = 100, cursor = cursor, returned_fields = ["email"])
        query = search.Query(
            query_string = 'NOT (tag = "Imabis-Import" OR tag = "Excel-Import")',
            options = options
        )

        results = index.search(query)
        cursor = results.cursor

        for document in results:
            doc_id = document.doc_id
            email = document.fields[0].value
            domain = email.split("@", 1)[1]
            
            if domain in [
                u'aon.at',
                u'gmx.at',
                u'hotmail.com',
                u'chello.at',
                u'gmail.com',
                u'yahoo.de',
                u'immoads.at',
                u'a1.net',
                u'gmx.net',
                u'utanet.at',
                u'liwest.at',
                u'inode.at',
                u'web.de',
                u'tele2.at',
                u't-online.de',
                u'oe24.at',
                u'gmx.com',
                u'yahoo.com',
                u'drei.at',
                u'yahoo.it',
                u'tirol.com',
                u'test.at',
                u'sms.at',
                u'rimml.com',
                u'outlook.com',
                u'justimmo.at',
            ]:
                continue
            
            domains = addresses.setdefault(doc_id, set())
            domains.add(domain)
            

            # deferred.defer(
            #     _do_iteration_part2,
            #     email = email,
            #     _queue = "noretry"
            # )

    
    
    domains = {}
    for address in addresses.values():
        for domain in address:
            domains[domain] = domains.get(domain, 0) + 1                
    
    
    
    domain_list = []
    for key, value in domains.items():
        domain_list.append((value, key))

    domain_list.sort(reverse = True)


    logging.info(domain_list)

    logging.info("Do-Iteration fertig")

    return True


def _do_iteration_part2(email):

    # E-Mail in (Imabix/Excel)-Import suchen
    result = common.addresses.get_addresses_by_search(
        page = 1,
        page_size = 100,
        query_string = u'email = "{email}" AND (tag = "Imabis-Import" OR tag = "Excel-Import")'.format(email = email),
    )
    for address in result["addresses"]:
        # Imabis/Excel-Adresse löschen
        logging.info("Adresse wird geloescht PROD")
        common.addresses.delete_address(
            user = "gerold",
            key_urlsafe = address.key.urlsafe(),
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
