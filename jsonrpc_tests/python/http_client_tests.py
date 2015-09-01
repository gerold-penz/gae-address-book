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
        kind = None,
        category_list = None,
        organization = None,
        position = None,
        salutation = None,
        first_name = None,
        last_name = None,
        nickname = None,
        street = None,
        postcode = None,
        city = None,
        district = None,
        land = None,
        country = None,
        phone_list = None,
        email_list = None,
        url_list = None,
        note_list = None,
        journal_list = None,
        business_list = None,
        anniversary_list = None,
        gender = None
    )

except pyjsonrpc.JsonRpcError, err:
    print err.code
    print err.message
    print err.data
