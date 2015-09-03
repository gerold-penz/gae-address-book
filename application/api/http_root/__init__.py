#!/usr/bin/env python
# coding: utf-8

# Namespace Imports
from jsonrpc import jsonrpc


import cherrypy


@cherrypy.expose
def testpage():
    raise RuntimeError(u"Österreich - GAE-Address-Book")
