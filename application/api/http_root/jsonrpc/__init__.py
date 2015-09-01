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
import common.addresses
import common.authorization
from common.model.address import (
    Tel, Email, Url, Note, Agreement, JournalItem, Anniversary
)


from mako.template import Template
from pyjsonrpc.cp import CherryPyJsonRpc, rpcmethod


THISDIR = os.path.dirname(os.path.abspath(__file__))


# Globale Variable um die Benutzer (threadübergreifend) zwischenzuspeichern
_users = None
_users_lock = threading.Lock()


def _security_users():
    """
    Liest die Benutzer aus der Scurity-INI aus uns speichert diese in einer
    globalen Variable zwischen.
    """

    global _users

    if _users:
        return _users

    with _users_lock:
        _users = {}
        for key, value in cherrypy.config["users"].items():
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
        "tools.basic_auth.users": _security_users
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


    @rpcmethod
    def create_address(
        self,
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
    ):
        """
        Creates a new address

        :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-*"
        :param category_list: A list of "tags" that can be used to describe the object.
        :param organization: Organization name or location name
        :param position: Specifies the job title, functional position or function of
            the individual within an organization.
        :param salutation: Salutation (Dr., Prof.)
        :param first_name: First name of a person
        :param last_name: Last name of a person
        :param nickname: Nickname
        :param street: Street and number
        :param postcode: Postcode/ZIP
        :param city: City/town/place
        :param district: Political district
        :param land: Bundesland (z.B. Tirol, Bayern)
        :param country: Staat (z.B. Österreich, Deutschland)

        :param phone_list: A list with dictionaries.
            Syntax::

                [{"label": "<name>", "number": "<number">}, ...]

            Example::

                [
                    {"label": "Mobile", "number": "+43 123 456 789"},
                    {"label": "Fax", "number": "+43 123 456 999"}
                ]

        :param email_list: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "email": "<email>"}, ...]

            Example::

                [
                    {"label": "Private", "email": "max.mustermann@private.com"},
                    {"label": "Business", "email": "m.mustermann@organization.com"}
                ]

        :param url_list: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "url": "<url>"}, ...]

            Example::

                [{"label": "Homepage", "url": "http://halvar.at/"}]

        :param note_list: A list with dictionaries.
            Syntax::

                [{"text": "<note>"}, ...]

            Example::

                [{"text": "This is a short note"}]


        :param journal_list: A list with dictionaries.
            Syntax::

                [{"date_time_iso": <DateTimeIso>, "text": "<note>"), ...]

            Example::

                [
                    {
                        "date_time_iso": "2000-01-01T14:30",
                        "text": "This is a short journal item."
                    }, ...
                ]

        :param business_list: A list with strings.
            Example::

                ["carpenter", "furniture"]


        :param anniversary_list: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "year": <year>, "month": <month [1-12]>, "day": <day>}, ...]

            Example::

                [{"label": "Birthday", "year": 1974, "month": 8, "day": 18}, ...]

        :param gender: Defines the person's gender. A single letter.
            M stands for "male",
            F stands for "female",
            O stands for "other",
            N stands for "none or not applicable",
            U stands for "unknown"
        """

        # Username
        user = cherrypy.request.login




        # Create new address
        new_address = common.addresses.create(
            user = user,
            kind = None,
            category_items = None,
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
            phone_items = None,
            email_items = None,
            url_items = None,
            note_items = None,
            journal_items = None,
            business_items = None,
            anniversary_items = None,
            gender = None
        )






def jronsrpc_help(*args, **kwargs):
    """
    Gibt eine Hilfe-Seite zurück
    """

    # Vorlage
    template_path = os.path.join(THISDIR, "help.mako")
    template = Template(filename = template_path)
    rendered = template.render_unicode(
        version = common.constants.VERSION,
        appname = cherrypy.config["appname"],
        add_doc = extract_documentation(JsonRpc.add, u"add")
    )

    # Fertig
    return rendered


jsonrpc = JsonRpc()
jsonrpc.help = jronsrpc_help
jsonrpc.help._cp_config = {"tools.basic_auth.on": False}
jsonrpc.help.exposed = True


