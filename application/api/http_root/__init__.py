#!/usr/bin/env python
# coding: utf-8


import datetime
import cherrypy
import common.addresses
import common.http


# Namespace Imports
from jsonrpc import jsonrpc


@cherrypy.expose
def test():

    new_address = common.addresses.create(
        user = u"test",
        kind = u"individual",
        category_items = [
            u"Test1", u"Test2", u"Österreich"
        ],
        organization = u"GP-COM",
        position = u"Lehrling",
        salutation = u"Prof.",
        first_name = u"Gerold",
        last_name = u"Penz",
        nickname = u"Halvar",
        street = u"Bahnhofstraße 15 d",
        postcode = u"6410",
        city = u"Telfs",
        district = u"Innsbruck-Land",
        land = u"Tirol",
        country = u"Österreich",
        phone_items = [
            common.addresses.Tel(
                label = u"Mobil", number = u"+43 123 456 789"
            )
        ],
        email_items = [
            common.addresses.Email(
                label = u"Privat", email = u"gerold@halvar.at"
            )
        ],
        url_items = [
            common.addresses.Url(
                label = u"Private Homepage", url = u"http://halvar.at"
            )
        ],
        note_items = [
            common.addresses.Note(
                text = u"Das ist eine Testnotiz"
            )
        ],
        journal_items = [
            common.addresses.JournalItem(
                date_time = datetime.datetime(2000, 1, 1, 10, 20),
                text = u"Das ist ein Journaleintrag"
            )
        ],
        business_items = [
            u"Tischler", u"Möbel", u"Küchen"
        ],
        anniversary_items = [
            common.addresses.Anniversary(
                label = u"Geburtstag",
                year = 1974,
                month = 8,
                day = 18
            )
        ],
        gender = "M"

    )

    common.http.set_content_type_text()
    return repr(new_address)
