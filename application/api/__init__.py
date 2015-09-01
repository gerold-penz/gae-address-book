#!/usr/bin/env python
# coding: utf-8

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
APPLICATIONDIR = os.path.abspath(os.path.join(THISDIR, ".."))
sys.path.insert(0, APPLICATIONDIR)
sys.path.insert(0, THISDIR)

import cherrypy
import common.constants
import lib.constants


# Namespace-Imports
import http_root
import error_pages


def get_app():
    """
    Gibt die Cherrypy-Application für die JSONRPC-Api zurück
    """

    app = cherrypy.Application(http_root, "/api")

    # cherrypy.config
    cherrypy_config = {

        # Produktivumgebung
        "environment": "production",
        "log.screen": False,
        "request.show_tracebacks": False,
        "request.show_mismatched_params": False,

        # Encoding der auszuliefernden HTML-Seiten
        "tools.encode.on": True,
        "tools.encode.encoding": "utf-8",
        "tools.decode.on": True,

        # Error-Page(s)
        "error_page.500": error_pages.error_page_500,
        "error_page.404": error_pages.error_page_404,
    }

    cherrypy.config.update(cherrypy_config)
    cherrypy.config.update(common.constants.COMMON_INIPATH)
    cherrypy.config.update(lib.constants.SECURITY_INIPATH)

    # app.config
    app_config = {
        "/": {
            # Error-Page(s)
            "error_page.500": error_pages.error_page_500,
            "error_page.404": error_pages.error_page_404,
            # URL Anpassung
            "tools.trailing_slash.on": False,
        },
    }
    app.config.update(app_config)
    app.merge(common.constants.COMMON_INIPATH)
    app.merge(lib.constants.SECURITY_INIPATH)

    # Fertig
    return app


app = get_app()

