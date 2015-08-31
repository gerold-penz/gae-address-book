#!/usr/bin/env python
# coding: utf-8

import os
import cherrypy
import hashlib
import threading
import inspect
import docutils
import docutils.core
import common.constants
import common.format_
from mako.template import Template
from pyjsonrpc.cp import CherryPyJsonRpc, rpcmethod


THISDIR = os.path.dirname(os.path.abspath(__file__))


# Globale Variable um die Benutzer (threadübergreifend) zwischenzuspeichern
_users = None
_users_lock = threading.Lock()


def _api_users():
    """
    Liest die API-Benutzer aus der INI aus uns speichert diese in einer
    globalen Variable zwischen.
    """

    global _users

    if _users:
        return _users

    with _users_lock:
        _users = {}
        for key, value in cherrypy.config["api.jsonrpc.users"].items():
            _users[key] = hashlib.md5(value).hexdigest()

    return _users


def rest2html(
    input_string, input_encoding = "utf-8", output_encoding = "utf-8",
    doctitle = 0, initial_header_level = 2, language_code = "de"
):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> tag, less the title,
    subtitle, and docinfo.
    """

    if not isinstance(input_string, unicode):
        if callable(input_string):
            input_string = str(input_string())
        input_string = unicode(input_string, input_encoding, "replace")

    overrides = {
        "input_encoding": "unicode",
        "doctitle_xform": doctitle,
        "initial_header_level": initial_header_level,
        "language_code": language_code,
        "field_name_limit": 0,
    }
    parts = docutils.core.publish_parts(
        source = input_string, writer_name='html', settings_overrides = overrides
    )
    fragment = parts['fragment']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding, "replace")

    return fragment


def extract_documentation(python_object, name):
    """
    Holt sich die Docstrings und wandelt diese in einen HTML-String um
    """

    template_str = ""
    docstring = inspect.getdoc(python_object)

    if docstring:
        template_str += u'<div class="method">'
        template_str += u'<h3>%s(%s)</h3>\n' % (
            name, u", ".join(
                item for item in inspect.getargspec(python_object)[0]
                if not item == "self"
            )
        )
        template_str += rest2html(
            docstring,
            output_encoding = "unicode",
            initial_header_level = 4
        )
        template_str += u'</div>'

    # Fertig
    return template_str


class JsonRpc(CherryPyJsonRpc):
    """
    JsonRpc-Api-Zugang
    """

    _cp_config = {
        "tools.basic_auth.on": True,
        "tools.basic_auth.realm": "GAE-Address-Book - JSON-RPC API",
        "tools.basic_auth.users": _api_users
    }

    index = CherryPyJsonRpc.request_handler


    # TEST
    @rpcmethod
    def add(self, a, b):
        """
        Test method

        ==========
        Parameters
        ==========

        :param a: Any value

        :param b: Any value

        :return: Result of ``a + b``.
        """

        return a + b


def jronsrpc_help(*args, **kwargs):
    """
    Gibt eine Hilfe-Seite zurück
    """

    # Vorlage
    template_path = os.path.join(THISDIR, "help.mako")
    template = Template(filename = template_path)
    rendered = template.render_unicode(
        version = common.constants.VERSION,
        appname = cherrypy.config["APPNAME"],
        add_doc = extract_documentation(JsonRpc.add, u"add")
    )

    # Fertig
    return rendered


jsonrpc = JsonRpc()
jsonrpc.help = jronsrpc_help
jsonrpc.help._cp_config = {"tools.basic_auth.on": False}
jsonrpc.help.exposed = True


