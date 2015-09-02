#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


# TEST ENVIRONMENT
address_book = pyjsonrpc.HttpClient(
    url = "http://localhost:8080/api/jsonrpc",
    username = "test",
    password = "test"
)

try:
    print address_book.create_address(
        kind = u"individual",
        category_list = [u"Test1", u"Test2", u"Österreich"],
        organization = u"GP-COM",
        position = u"Lehrling",
        salutation = None,
        first_name = u"Gerold",
        last_name = u"Penz",
        nickname = u"Halvar",
        street = u"Anystreet 11",
        postcode = u"Anypostcode",
        city = u"Anycity",
        district = u"Innsbruck-Land",
        land = u"Tirol",
        country = u"Österreich",
        phone_list = [
            {"label": u"Mobil", "number": u"+43 123 456 789"}
        ],
        email_list = [
            dict(label = u"Privat", email = u"gerold@halvar.at")
        ],
        url_list = [
            dict(label = u"Private Homepage", url = u"http://halvar.at")
        ],
        note_list = [
            dict(text = u"Das ist eine Testnotiz")
        ],
        journal_list = [
            dict(
                date_time_iso = "2000-01-01T10:20:00",
                text = u"Das ist ein Journaleintrag"
            )
        ],
        business_list = [u"Tischler", u"Möbel", u"Küchen"],
        anniversary_list = [
            dict(
                label = u"Geburtstag",
                year = 1974,
                month = 8,
                day = 18
            )
        ],
        gender = "M"
    )

except pyjsonrpc.JsonRpcError, err:
    print err.code
    print err.message
    print err.data
