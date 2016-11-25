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

        options = search.QueryOptions(limit = 400, cursor = cursor, ids_only = True)

        query_string = " OR ".join([
            'email = "{email}"'.format(email = email) for email in [
                "@ivcon.at",
                "@era.at",
                "@sreal.at",
                "@remax-dci.at",
                "@dmh.co.at",
                "@remax-pi.at",
                "@remax-classic.at",
                "@remax-4you.at",
                "@realkanzlei-mayerl.at",
                "@immofair.at",
                "@immo-contract.com",
                "@firstclassreal.at",
                "@wohneschoener.at",
                "@vilu.at",
                "@trendimmobilien.at",
                "@stadtquartier.at",
                "@rtm.at",
                "@remax-plus.at",
                "@remax-homes.at",
                "@remax-first.at",
                "@planquadrat.cc",
                "@neuhauser-immobilien.at",
                "@moneypower.at",
                "@mb-immoservice.net",
                "@linecker-partner.at",
                "@immotrends.com",
                "@immopunkt.at",
                "@immogrand.at",
                "@immobilias.at",
                "@immobex.at",
                "@immo-top.at",
                "@haiden-immo.at",
                "@forliving.at",
                "@fischerimmo.at",
                "@fhi.at",
                "@esprit-immo.at",
                "@dreamfactory.at",
                "@drako-immobilien.at",
                "@bkf.at",
                "@wohntraumreal.at",

                # "@wohnimpuls.co.at",
                # "@wohnen-wert.at",
                # "@wohnbau2000.at",
                # "@wohn3.at",
                # "@wohn-salon.at",
                # "@wimmer-immobilien.at",
                # "@wien-wohnungen.at",
                # "@wertimmobilien.at",
                # "@wbimmo.at",
                # "@w-i-r.at",
                # "@vkb-bank.at",
                # "@viste-immobilien.at",
                # "@umhaeuserbesser.at",
                # "@triangolo-immo.com",
                # "@transimmobil.at",
                # "@tmu-real.at",
                # "@tmo.at",
                # "@teamreal.at",
                # "@teamneunzehn.at",
                # "@stibi-immo.at",
                # "@stengg-invest.at",
                # "@seereal.at",
                # "@seebacher-immo.at",
                # "@schuster.at",
                # "@schmoellers.at",
                # "@schatz-immobilien.at",
                # "@sattmann-immobilien.at",
                # "@riedergarten.at",
                # "@remaxuno.at",
                # "@remax.net",
                # "@remax-whitehorse.at",
                # "@remax-viva.at",
                # "@remax-vision.at",
                # "@remax-traunsee.at",
                # "@remax-living.at",
                # "@remax-leibnitz.at",
                # "@remax-impuls.at",
                # "@remax-immoteam.at",
                # "@remax-graz-sued.at",
                # "@remax-gold.at",
                # "@remax-fair.at",
                #
                # "@remax-countrylife.at",
                # "@remax-bad-ischl.at",
                # "@remax-alpin.at",
                # "@remax-alpha.at",
                # "@reischauer.at",
                # "@regus.com",
                # "@referenz-immobilien.at",
                # "@realis-consulting.at",
                # "@raab.at",
                # "@protop.com",
                # "@pro-real.at",
                # "@primmobilien.at",
                # "@preiml.com",
                # "@power-immobilien.at",
                # "@polke-partner.at",
                # "@planflexx.com",
                # "@permoser.co.at",
                # "@pegra.net",
                # "@optima-casa.at",
                # "@oeser.at",
                # "@novaconsult.at",
                # "@nageler.biz",
                # "@msn.com",
                # "@mfimmobilien.at",
                # "@mauhart.at",
                # "@marek-immobilien.at",
                # "@kstp.at",
                # "@krutzler.net",
                # "@kpimmo.at",
                # "@kogler-immobilien.at",
                # "@km-real.at",
                # "@kk-immo.at",
                # "@kirnberger.com",
                # "@khimmobilien.at",
                # "@kalandra.at",
                # "@kaempf.at",
                # "@jes-invest.at",
                # "@jansa-immobilien.at",
                # "@isidex.at",
                # "@ipc-immo.com",
                # "@immovativ.at",
                # "@immothek.at",
                # "@immoshop.at",
                #
                # "@immoservice.or.at",
                # "@immosbg.at",
                # "@immoplex.at",
                # "@immopartner.net",
                # "@immobility.co.at",
                # "@immobilien-treuhand.com",
                # "@immobilien-schweighofer.at",
                # "@immobilien-salzburg.org",
                # "@immobilien-ribarits.at",
                # "@immo-stabil.at",
                # "@immo-spannring.at",
                # "@immo-brunner.at",
                # "@immo-blaskovic.at",
                # "@ilba.at",
                # "@ideal-real.com",
                # "@icimmo.at",
                # "@i-sp.at",
                # "@horicon.at",
                # "@hoffmann-immobilien.at",
                # "@hinteregger-immobilien.at",
                # "@hierwohnich.at",
                # "@herar-immo.at",
                # "@heissimmobilien.at",
                # "@heiku-immobilien.at",
                # "@haslehner.net",
                # "@haring-group.at",
                # "@gross-klein.at",
                # "@gpimmo.at",
                # "@gmx.de",
                # "@gmk.at",
                # "@glorit.at",
                # "@georeal.info",
                # "@friends-immobilien.at",
                # "@friedrich-immo.at",
                # "@filmconsult.at",
                # "@fidelitas.at",
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
    tag_items.append("In-Bearbeitung")

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
