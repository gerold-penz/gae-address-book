#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


# TEST ENVIRONMENT
address_book = pyjsonrpc.HttpClient(
    url = "http://localhost:8081/api/jsonrpc",
    username = "test",
    password = "test"
)


try:
    print address_book.get_info()
except pyjsonrpc.JsonRpcError, err:
    print err.code
    print err.message
    print err.data
