#!/usr/bin/env python
# coding: utf-8
"""
Error Pages
"""

import os
import cherrypy
import logging
import common.format_
from mako.template import Template

THISDIR = os.path.dirname(os.path.abspath(__file__))


def error_page_500(status, message, traceback, version):
    """
    Standard- Fehlerseite

    > cherrypy.config.update({"error_page.500": error_page_500})
    """

    try:

        # Vorlage
        template_path = os.path.join(THISDIR, "error_page_500.mako")
        template = Template(filename = template_path)

        # Vorlage rendern
        rendered = template.render_unicode(
            status = common.format_.safe_unicode(status),
            message = common.format_.safe_unicode(message),
            traceback = common.format_.safe_unicode(traceback),
            version = common.format_.safe_unicode(version)
        )

        # Fertig
        cherrypy.response.body = rendered
        return rendered

    except StandardError, err:
        logging.error(" ")
        logging.error(u"--------------------------------------------")
        logging.error(u"--- SCHWERER FEHLER in Fehlerseite - 500 ---")
        logging.error(common.format_.safe_unicode(err))
        logging.error(common.format_.get_traceback_string())
        logging.error(u"--- SCHWERER FEHLER in Fehlerseite - 500 ---")
        logging.error(u"--------------------------------------------")
        logging.error(" ")


def error_page_404(status, message, traceback, version):
    """
    Standard- Fehlerseite

    > cherrypy.config.update({"error_page.404": error_page_404})
    """

    try:

        # Vorlage
        template_path = os.path.join(THISDIR, "error_page_404.mako")
        template = Template(filename = template_path)

        # Vorlage rendern
        rendered = template.render_unicode(
            status = common.format_.safe_unicode(status),
            message = common.format_.safe_unicode(message),
            traceback = common.format_.safe_unicode(traceback),
            version = common.format_.safe_unicode(version)
        )

        # Fertig
        cherrypy.response.body = rendered
        return rendered

    except StandardError, err:
        logging.error(" ")
        logging.error(u"--------------------------------------------")
        logging.error(u"--- SCHWERER FEHLER in Fehlerseite - 404 ---")
        logging.error(common.format_.safe_unicode(err))
        logging.error(common.format_.get_traceback_string())
        logging.error(u"--- SCHWERER FEHLER in Fehlerseite - 404 ---")
        logging.error(u"--------------------------------------------")
        logging.error(" ")

