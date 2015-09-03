#!/usr/bin/env python
# coding: utf-8

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))
APPLICATIONDIR = os.path.abspath(os.path.join(THISDIR, ".."))
sys.path.insert(0, APPLICATIONDIR)
sys.path.insert(0, THISDIR)

import cherrypy
import logging
import common.constants
import common.email
import lib.constants


# Namespace-Imports
import http_root
import error_pages


def email_tracebacks(severity = logging.CRITICAL):
    """
    Write the last error's headers and traceback to the cherrypy error log
    witih a ERROR severity.
    """

    h = ["  %s: %s" % (repr(k), repr(v)) for k, v in cherrypy.request.header_list]
    logstr = (
        "\nRequest Headers:\n" +
        "\n".join(h) +
        "\n\n" +
        repr(cherrypy._cperror.format_exc()).replace("\\n", "\n")
    )

    logstr += "\n" + ("-" * 60) + "\n"
    params_repr = repr(cherrypy.request.params)
    if len(params_repr) > 1000:
        params_repr = params_repr[:1000] + "..."
    logstr += "params: " + params_repr + "\n"
    logstr += "path_info: " + repr(cherrypy.request.path_info) + "\n"

    # # Erweitertes Traceback
    # logstr += (
    #     "\n\n" +
    #     "-" * 60 +
    #     "\n\n\n"
    # )
    # for key, value in cherrypy.request.__dict__.items():
    #     if key in ["config"]:
    #         continue
    #     logstr += "%s: %s\n\n" % (key, pformat(value).replace("\\n", "\n"))

    cherrypy.log(logstr, "HTTP", severity=severity)

cherrypy.tools.email_tracebacks = cherrypy.Tool('before_error_response', email_tracebacks)


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
        "tools.email_tracebacks.on": True,

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

    # Logging per Email
    if cherrypy.config.get("tools.email_tracebacks.on"):
        # set up an SMTP handler to mail when the WARNING error occurs
        gae_smtp_handler = common.email.GaeSmtpHandler(
            subject = "CherryPy Error - {APPNAME}".format(
                APPNAME = cherrypy.config["APPNAME"]
            )
        )
        gae_smtp_handler.setLevel(logging.CRITICAL)
        cherrypy.log.error_log.addHandler(gae_smtp_handler)

    # Fertig
    return app


app = get_app()

