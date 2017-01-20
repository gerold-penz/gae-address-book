#!/usr/bin/env python
# coding: utf-8

import os
import cherrypy
import hashlib
import threading
import inspect
import docutils
import docutils.core
import datetime
import common.constants
import common.format_
import common.addresses
import common.authorization
import common.tag_items
import common.category_items
import common.business_items
import common.free_defined_fields
from mako.template import Template
from pyjsonrpc import JsonRpcError
from google.appengine.api import search
from pyjsonrpc.cp import CherryPyJsonRpc, rpcmethod


THISDIR = os.path.dirname(os.path.abspath(__file__))
QUERY_ERROR = 1001



# Globale Variable um die Benutzer (threadübergreifend) zwischenzuspeichern
_users = None
_users_lock = threading.Lock()


def _security_users():
    """
    Returns the users (security.ini)
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
        function_help_strings = [
            # Help strings
            extract_documentation(JsonRpc.get_info, u"get_info"),

            extract_documentation(JsonRpc.create_address, u"create_address"),
            extract_documentation(JsonRpc.get_address, u"get_address"),
            extract_documentation(JsonRpc.save_address, u"save_address"),
            extract_documentation(JsonRpc.delete_address, u"delete_address"),
            extract_documentation(JsonRpc.get_addresses, u"get_addresses"),
            extract_documentation(JsonRpc.search_addresses, u"search_addresses"),

            extract_documentation(JsonRpc.get_category_items, u"get_category_items"),
            extract_documentation(JsonRpc.get_business_items, u"get_business_items"),
            extract_documentation(JsonRpc.get_tag_items, u"get_tag_items"),

            extract_documentation(JsonRpc.create_free_defined_field, u"create_free_defined_field"),
            extract_documentation(JsonRpc.get_free_defined_field, u"get_free_defined_field"),
            extract_documentation(JsonRpc.save_free_defined_field, u"save_free_defined_field"),
            extract_documentation(JsonRpc.delete_free_defined_field, u"delete_free_defined_field"),
            extract_documentation(JsonRpc.get_free_defined_fields, u"get_free_defined_fields"),

            extract_documentation(JsonRpc.start_refresh_index, u"start_refresh_index"),
            extract_documentation(JsonRpc.start_delete_all_addresses, u"start_delete_all_addresses"),
            extract_documentation(JsonRpc.start_delete_all_search_indexes, u"start_delete_all_search_indexes"),

            extract_documentation(JsonRpc.get_search_index_fieldnames, u"get_search_index_fieldnames"),


        ]
    )

    # Finished
    return rendered


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


    @rpcmethod
    def get_info(self):
        """
        Returns informations about the address book
        """

        # Finished
        return dict(
            appname = cherrypy.config["APPNAME"],
            label = cherrypy.config["LABEL"],
            addresses_count = common.addresses.get_address_quantity_cached()
        )


    @rpcmethod
    def create_address(
        self,
        kind = None,
        category_items = None,
        tag_items = None,
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
        agreement_items = None,
        free_defined_items = None,
        business_items = None,
        anniversary_items = None,
        gender = None
    ):
        """
        Creates a new address

        ==========
        Parameters
        ==========

        :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-\*"
        :param category_items: A list with "tags" that can be used to describe the object.
        :param tag_items: A list with "tags" that can be used to describe the object.
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

        :param phone_items: A list with dictionaries.
            Syntax::

                [{"label": "<name>", "number": "<number">}, ...]

            Example::

                [
                    {"label": "Mobile", "number": "+43 123 456 789"},
                    {"label": "Fax", "number": "+43 123 456 999"}
                ]

        :param email_items: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "email": "<email>"}, ...]

            Example::

                [
                    {"label": "Private", "email": "max.mustermann@private.com"},
                    {"label": "Business", "email": "m.mustermann@organization.com"}
                ]

        :param url_items: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "url": "<url>"}, ...]

            Example::

                [{"label": "Homepage", "url": "http://halvar.at/"}]

        :param note_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"}, ...]

            Example::

                [{"text": "This is a short note"}]


        :param journal_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"), ...]

            Example::

                [{"text": "This is a short journal item"}]

        :param agreement_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"), ...]

            Example::

                [{"text": "This is a short agreement item"}]

        :param free_defined_items: A list with dictionaries.
            Syntax::

                [{"group": "<group name>", "label": "<label>", "text": "<text>", value_type = "unicode"|"int"|"float"|"date"), ...]

            Example::

                [
                    {"group": "Body Data", "label": "Shoe-Size", "text": "45", value_type = "unicode"},
                    {"group": "Body Data", "label": "Body-Height", "text": "180", value_type = "unicode"}
                ]

        :param business_items: A list with strings.
            Example::

                ["carpenter", "furniture"]


        :param anniversary_items: A list with dictionaries.
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

        :return: New address (dictionary)
        """

        # Username
        user = cherrypy.request.login

        # Prepare Phone-Items
        if phone_items:
            phone_items = [
                common.addresses.TelItem(**phone_item) for phone_item in phone_items
            ]

        # Prepare Email-Items
        if email_items:
            email_items = [
                common.addresses.EmailItem(**email_item) for email_item in email_items
            ]

        # Prepare Url-Items
        if url_items:
            url_items = [
                common.addresses.UrlItem(**url_item) for url_item in url_items
            ]

        # Prepare Note-Items
        if note_items:
            note_items = [
                common.addresses.NoteItem(**note_item) for note_item in note_items
            ]

        # Prepare Journal-Items
        if journal_items:
            journal_items = [
                common.addresses.JournalItem(**journal_item) for
                journal_item in journal_items
            ]

        # Prepare Agreement-Items
        if agreement_items:
            agreement_items = [
                common.addresses.AgreementItem(**agreement_item) for
                agreement_item in agreement_items
            ]

        # Prepare FreeDefinedItems
        if free_defined_items:
            free_defined_items = [
                common.addresses.FreeDefinedItem(**free_defined_item) for
                free_defined_item in free_defined_items
            ]

        # Prepare Anniversary-Items
        if anniversary_items:
            anniversary_items = [
                common.addresses.AnniversaryItem(**anniversary_item) for
                anniversary_item in anniversary_items
            ]

        # Create new address
        new_address = common.addresses.create(
            user = user,
            kind = kind,
            category_items = category_items,
            tag_items = tag_items,
            organization = organization,
            position = position,
            salutation = salutation,
            first_name = first_name,
            last_name = last_name,
            nickname = nickname,
            street = street,
            postcode = postcode,
            city = city,
            district = district,
            land = land,
            country = country,
            phone_items = phone_items,
            email_items = email_items,
            url_items = url_items,
            note_items = note_items,
            journal_items = journal_items,
            agreement_items = agreement_items,
            free_defined_items = free_defined_items,
            business_items = business_items,
            anniversary_items = anniversary_items,
            gender = gender
        )

        # Finished
        return new_address.to_dict()


    @rpcmethod
    def get_addresses(
        self,
        page = 1,
        page_size = 20,
        include = None,
        exclude = None,
        exclude_creation_metadata = None,
        exclude_edit_metadata = None,
        exclude_empty_fields = None,
        order_by = None,
        query_string = None,
        filter_by_organization = None,
        filter_by_organization_char1 = None,
        filter_by_first_name = None,
        filter_by_first_name_char1 = None,
        filter_by_last_name = None,
        filter_by_last_name_char1 = None,
        filter_by_nickname = None,
        filter_by_nickname_char1 = None,
        filter_by_street = None,
        filter_by_street_char1 = None,
        filter_by_postcode = None,
        filter_by_postcode_char1 = None,
        filter_by_city = None,
        filter_by_city_char1 = None,
        filter_by_business_items = None,
        filter_by_category_items = None,
        filter_by_tag_items = None
    ):
        """
        Returns a dictionary with the count of addresses and one page of addresses

        All *datetime.date*- and *datetime.datetime*-values will convert to
        ISO date strings.

        :param page: Page to fetch

        :param page_size: Page size

        :param include: Optional list of properties to include. Default: all.

        :param exclude: Optional list of properties to exclude.
            If there is overlap between include and exclude, then exclude "wins."

        :param exclude_creation_metadata: If `True`, the fields "ct" (creation timestamp)
            and "cu" (creation user) will excluded

        :param exclude_edit_metadata: If `True`, the fields "et" (creation timestamp)
            and "eu" (creation user) will excluded.

        :param order_by: Order result, String or list with fieldnames. A "-"
            sets descending order.

        :param filter_by_name: Case insensitive filter string which filters the
            fields "organization", "first_name", "last_name".

        :param filter_by_place: Case insensitive filter string which filters the
            fields "street", "postcode", "city", "country", "land", "district".

        :param filter_by_category_items: List with *case sensitive* items.

        :param filter_by_tag_items: List with *case sensitive* items.

        :param filter_by_business_items: List with *case sensitive* items.

        :return: Dictionary with total quantity and one page with addresses::

            {
                "total_quantity": <Quantity>,
                "addresses": [<Address>, ...]
            }
        """

        addresses = []

        try:
            fetched_result = common.addresses.get_addresses_by_search(
                page = page,
                page_size = page_size,
                order_by = order_by,
                query_string = query_string,
                filter_by_organization = filter_by_organization,
                filter_by_organization_char1 = filter_by_organization_char1,
                filter_by_first_name = filter_by_first_name,
                filter_by_first_name_char1 = filter_by_first_name_char1,
                filter_by_last_name = filter_by_last_name,
                filter_by_last_name_char1 = filter_by_last_name_char1,
                filter_by_nickname = filter_by_nickname,
                filter_by_nickname_char1 = filter_by_nickname_char1,
                filter_by_street = filter_by_street,
                filter_by_street_char1 = filter_by_street_char1,
                filter_by_postcode = filter_by_postcode,
                filter_by_postcode_char1 = filter_by_postcode_char1,
                filter_by_city = filter_by_city,
                filter_by_city_char1 = filter_by_city_char1,
                filter_by_business_items = filter_by_business_items,
                filter_by_category_items = filter_by_category_items,
                filter_by_tag_items = filter_by_tag_items
            )
        except search.Error as err:
            raise JsonRpcError(
                message = common.format_.safe_errormessage(err),
                code = QUERY_ERROR
            )

        for address in fetched_result["addresses"]:
            addresses.append(address.to_dict(
                include = include,
                exclude = exclude,
                exclude_creation_metadata = exclude_creation_metadata,
                exclude_edit_metadata = exclude_edit_metadata,
                exclude_empty_fields = exclude_empty_fields
            ))

        # Finished
        return dict(
            total_quantity = fetched_result["total_quantity"],
            addresses = addresses
        )


    @rpcmethod
    def get_address(
        self,
        key_urlsafe = None,
        address_uid = None,
        include = None,
        exclude = None,
        exclude_creation_metadata = None,
        exclude_edit_metadata = None,
        exclude_empty_fields = None
    ):
        """
        Returns all data for the requested address

        :param include: Optional list of properties to include. Default: all.

        :param exclude: Optional list of properties to exclude.
            If there is overlap between include and exclude, then exclude "wins."

        :param exclude_creation_metadata: If `True`, the fields "ct" (creation timestamp)
            and "cu" (creation user) will excluded

        :param exclude_edit_metadata: If `True`, the fields "et" (creation timestamp)
            and "eu" (creation user) will excluded.
        """

        address = common.addresses.get_address(
            key_urlsafe = key_urlsafe,
            address_uid = address_uid
        )
        if not address:
            return None

        address_dict = address.to_dict(
            include = include,
            exclude = exclude,
            exclude_creation_metadata = exclude_creation_metadata,
            exclude_edit_metadata = exclude_edit_metadata,
            exclude_empty_fields = exclude_empty_fields
        )

        # Finished
        return address_dict


    @rpcmethod
    def start_refresh_index(self):
        """
        Starts the refreshing of the index in a query (deferred)
        """

        # Address index refresh
        common.addresses.start_refresh_index()

        # Finished
        return True


    @rpcmethod
    def save_address(
        self,
        key_urlsafe = None,
        address_uid = None,
        owner = None,
        kind = None,
        category_items = None,
        tag_items = None,
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
        agreement_items = None,
        free_defined_items = None,
        business_items = None,
        anniversary_items = None,
        gender = None
    ):
        """
        Saves one address

        The original address will saved into the *address_history*-table before.

        ==========
        Parameters
        ==========

        :param owner: The username of the owner
        :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-\*"
        :param category_items: A list of "tags" that can be used to describe the object.
        :param tag_items: A list of "tags" that can be used to describe the object.
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

        :param phone_items: A list with dictionaries.
            Syntax::

                [{"label": "<name>", "number": "<number">}, ...]

            Example::

                [
                    {"label": "Mobile", "number": "+43 123 456 789"},
                    {"label": "Fax", "number": "+43 123 456 999"}
                ]

        :param email_items: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "email": "<email>"}, ...]

            Example::

                [
                    {"label": "Private", "email": "max.mustermann@private.com"},
                    {"label": "Business", "email": "m.mustermann@organization.com"}
                ]

        :param url_items: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "url": "<url>"}, ...]

            Example::

                [{"label": "Homepage", "url": "http://halvar.at/"}]

        :param note_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"}, ...]

            Example::

                [{"text": "This is a short note"}]


        :param journal_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"), ...]

            Example::

                [{"text": "This is a short journal item"}]

        :param agreement_items: A list with dictionaries.
            Syntax::

                [{"text": "<text>"), ...]

            Example::

                [{"text": "This is a short agreement item"}]

        :param free_defined_items: A list with dictionaries.
            Syntax::

                [{"label": "<label>", "text": "<text>", value_type = "unicode"|"int"|"float"|"date"}, ...]

            Example::

                [
                    {"label": "Shoe-Size", "text": "45", value_type = "unicode"},
                    {"label": "Body-Height", "text": "180", value_type = "unicode"}
                ]

        :param business_items: A list with strings.
            Example::

                ["carpenter", "furniture"]


        :param anniversary_items: A list with dictionaries.
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

        :return: Saved address (dictionary)
        """

        # Username
        user = cherrypy.request.login

        # Prepare Phone-Items
        if phone_items:
            phone_items = [
                common.addresses.TelItem(**phone_item) for phone_item in phone_items
            ]

        # Prepare Email-Items
        if email_items:
            email_items = [
                common.addresses.EmailItem(**email_item) for email_item in email_items
            ]

        # Prepare Url-Items
        if url_items:
            url_items = [
                common.addresses.UrlItem(**url_item) for url_item in url_items
            ]

        # Prepare Note-Items
        if note_items:
            note_items = [
                common.addresses.NoteItem(**note_item) for note_item in note_items
            ]

        # Prepare Journal-Items
        if journal_items:
            journal_items = [
                common.addresses.JournalItem(**journal_item) for
                journal_item in journal_items
            ]

        # Prepare Agreement-Items
        if agreement_items:
            agreement_items = [
                common.addresses.AgreementItem(**agreement_item) for
                agreement_item in agreement_items
            ]

        # Prepare FreeDefined-Items
        if free_defined_items:

            for free_defined_item in free_defined_items:
                text = free_defined_item.get("text")
                if text is not None:
                    free_defined_item["text"] = unicode(text)

            free_defined_items = [
                common.addresses.FreeDefinedItem(**free_defined_item) for
                free_defined_item in free_defined_items
            ]

        # Prepare Anniversary-Items
        if anniversary_items:
            anniversary_items = [
                common.addresses.AnniversaryItem(**anniversary_item) for
                anniversary_item in anniversary_items
            ]

        # Saving
        address = common.addresses.save_address(
            user = user,
            key_urlsafe = key_urlsafe,
            address_uid = address_uid,
            owner = owner,
            kind = kind,
            category_items = category_items,
            tag_items = tag_items,
            organization = organization,
            position = position,
            salutation = salutation,
            first_name = first_name,
            last_name = last_name,
            nickname = nickname,
            street = street,
            postcode = postcode,
            city = city,
            district = district,
            land = land,
            country = country,
            phone_items = phone_items,
            email_items = email_items,
            url_items = url_items,
            note_items = note_items,
            journal_items = journal_items,
            agreement_items = agreement_items,
            free_defined_items = free_defined_items,
            business_items = business_items,
            anniversary_items = anniversary_items,
            gender = gender
        )

        address_dict = address.to_dict()

        # Finished
        return address_dict


    @rpcmethod
    def get_category_items(self):
        """
        Returns all used category items as unordered list.
        """

        # Finished
        return list(common.category_items.get_category_items_cached())


    @rpcmethod
    def get_business_items(self):
        """
        Returns all used business items as unordered list.
        """

        # Finished
        return list(common.business_items.get_business_items_cached())


    @rpcmethod
    def get_tag_items(self):
        """
        Returns cached tag items as unordered list.
        """

        # Finished
        return list(common.tag_items.get_tag_items_cached())


    @rpcmethod
    def search_addresses(
        self,
        query_string,
        page = None,
        page_size = None,
        returned_fields = None
    ):
        """
        Searches for addresses in the "Address" index

        :param query_string: Search string

        :param page: Page number

        :param page_size: Page size

        :param returned_fields: Field names of the result.
            Possible Field-Names:

            - kind
            - organization
            - position
            - salutation
            - first_name
            - last_name
            - nickname
            - street
            - postcode
            - city
            - district
            - land
            - country
            - gender
            - phone
            - email
            - url

        :return: Dictionary
            ::

                {
                    results: [
                        {
                            "doc_id": <KeyUrlsafe>,
                            "fields": [
                                {
                                    "name": <FieldName>,
                                    "value": <FieldValue>
                                },
                                ...
                            ]
                        },
                        ...
                    ],
                    "number_found": <quantity>
                }

        """

        # Search
        search_result = common.addresses.search_addresses(
            query_string = query_string,
            page = page or 1,
            page_size = page_size or 20,
            returned_fields = returned_fields
        )

        # Prepare result for converting to JSON
        result = dict(
            results = [],
            number_found = search_result.number_found
        )
        for scored_document in search_result.results:
            fields = []
            for field in scored_document.fields:
                value = field.value
                if isinstance(value, (datetime.date, datetime.datetime)):
                    value = value.isoformat()

                fields.append(dict(
                    name = field.name,
                    value = value
                ))
            document = dict(
                doc_id = scored_document.doc_id,
                fields = fields
            )
            result["results"].append(document)

        # Finished
        return result


    @rpcmethod
    def delete_address(
        self,
        key_urlsafe = None,
        address_uid = None,
        force = None
    ):
        """
        Deletes one address

        ==========
        Parameters
        ==========

        :param force: If `True`, the address will completely removed from the
            database, the address-history too.
            If `False`, the address will moved to the DeletedAddress-Model.
        """

        common.addresses.delete_address(
            user = cherrypy.request.login,
            key_urlsafe = key_urlsafe,
            address_uid = address_uid,
            force = force
        )

        # Finished
        return True


    @rpcmethod
    def create_free_defined_field(
        self,
        group,
        label,
        position = None,
        value_type = u"unicode",
    ):
        """
        Creates a new free defined field

        ==========
        Parameters
        ==========

        :param label: Label of the field
        :param group: Group name
        :param position: sort key
        :param value_type: "unicode"|"int"|"float"|"date"

        :return: New free defined field (dictionary)
        """

        # Username
        user = cherrypy.request.login

        # Create new free defined field
        new_free_defined_field = common.free_defined_fields.create(
            user = user,
            group = group,
            label = label,
            position = position,
            value_type = value_type
        )

        # Finished
        return new_free_defined_field.to_dict()


    @rpcmethod
    def delete_free_defined_field(self, key_urlsafe = None):
        """
        Deletes one free defined field
        """

        common.free_defined_fields.delete_free_defined_field(
            key_urlsafe = key_urlsafe
        )

        # Finished
        return True


    @rpcmethod
    def get_free_defined_field(self, key_urlsafe = None):
        """
        Returns all data for the requested free defined field
        """

        free_defined_field = common.free_defined_fields.get_free_defined_field(
            key_urlsafe = key_urlsafe
        )
        if not free_defined_field:
            return None

        free_defined_field_dict = free_defined_field.to_dict()

        # Finished
        return free_defined_field_dict


    @rpcmethod
    def get_free_defined_fields(
        self,
        exclude_creation_metadata = None
    ):
        """
        Returns a list with free defined fields

        :param exclude_creation_metadata: If `True`, the fields "ct" (creation timestamp)
            and "cu" (creation user) will excluded

        :return: List with free defined fields
        """

        free_defined_fields = []

        for free_defined_field in common.free_defined_fields.get_free_defined_fields():
            free_defined_fields.append(free_defined_field.to_dict(
                exclude_creation_metadata = exclude_creation_metadata
            ))

        # Finished
        return free_defined_fields


    @rpcmethod
    def save_free_defined_field(
        self,
        key_urlsafe = None,
        group = None,
        label = None,
        position = None,
        visible = None,
        value_type = u"unicode"
    ):
        """
        Saves one free_defined_field

        The original free defined field will saved before into the *free_defined_field_history*-table.

        ==========
        Parameters
        ==========

        :param group: Group name
        :param label: Label
        :param position: Sort key
        :param visible: Visibility of the field
        :param value_type: "unicode"|"int"|"float"|"date"

        :return: Saved free defined field (dictionary)
        """

        # Username
        user = cherrypy.request.login

        # Saving
        free_defined_field = common.free_defined_fields.save_free_defined_field(
            user = user,
            key_urlsafe = key_urlsafe,
            group = group,
            label = label,
            position = position,
            visible = visible,
            value_type = value_type
        )

        free_defined_field_dict = free_defined_field.to_dict()

        # Finished
        return free_defined_field_dict


    @rpcmethod
    def start_delete_all_addresses(self, yes_do_it = False):
        """
        Deletes ALL addresses. Really ALL!!!
        """

        if not yes_do_it:
            # Canceled
            return False

        # Delete all Addresses
        common.addresses.start_delete_all_addresses(yes_do_it = yes_do_it)

        # Finished
        return True


    @rpcmethod
    def start_delete_all_search_indexes(self, yes_do_it = False):
        """
        Deletes ALL search indexes. Really ALL!!!
        """

        if not yes_do_it:
            # Canceled
            return False

        # Delete all search indexes
        common.addresses.start_delete_all_search_indexes()

        # Finished
        return True


    @rpcmethod
    def get_search_index_fieldnames(self):
        """
        Returns the fieldnames of the "Address" search index
        """

        return common.addresses.get_search_index_fieldnames()


    @rpcmethod
    def get_addresses_for_iteration(
        self,
        cursor = None,
        limit = 100,
        include = None,
        exclude = None,
        exclude_creation_metadata = None,
        exclude_edit_metadata = None,
        exclude_empty_fields = None,
        order_by = None,
        query_string = None,
        filter_by_organization = None,
        filter_by_organization_char1 = None,
        filter_by_first_name = None,
        filter_by_first_name_char1 = None,
        filter_by_last_name = None,
        filter_by_last_name_char1 = None,
        filter_by_nickname = None,
        filter_by_nickname_char1 = None,
        filter_by_street = None,
        filter_by_street_char1 = None,
        filter_by_postcode = None,
        filter_by_postcode_char1 = None,
        filter_by_city = None,
        filter_by_city_char1 = None,
        filter_by_business_items = None,
        filter_by_category_items = None,
        filter_by_tag_items = None
    ):
        """
        Returns a dictionary with the count of addresses and one page of addresses

        All *datetime.date*- and *datetime.datetime*-values will convert to
        ISO date strings.

        :param cursor: Cursor-String for iteration over the full result

        :param limit: Maximum quantity of addresses in result

        :param include: Optional list of properties to include. Default: all.

        :param exclude: Optional list of properties to exclude.
            If there is overlap between include and exclude, then exclude "wins."

        :param exclude_creation_metadata: If `True`, the fields "ct" (creation timestamp)
            and "cu" (creation user) will excluded

        :param exclude_edit_metadata: If `True`, the fields "et" (creation timestamp)
            and "eu" (creation user) will excluded.

        :param order_by: Order result, String or list with fieldnames. A "-"
            sets descending order.

        :param query_string: Query string

        :param filter_by_name: Case insensitive filter string which filters the
            fields "organization", "first_name", "last_name".

        :param filter_by_place: Case insensitive filter string which filters the
            fields "street", "postcode", "city", "country", "land", "district".

        :param filter_by_category_items: List with *case sensitive* items.

        :param filter_by_tag_items: List with *case sensitive* items.

        :param filter_by_business_items: List with *case sensitive* items.

        :return: Dictionary with total quantity, cursor-string and one page
            with addresses::

                {
                    "total_quantity": <Quantity>,
                    "next_cursor": <CursorString>
                    "addresses": [<Address>, ...]
                }
        """

        addresses = []

        try:
            fetched_result = common.addresses.get_addresses_for_iteration(
                cursor = cursor,
                limit = limit,
                order_by = order_by,
                query_string = query_string,
                filter_by_organization = filter_by_organization,
                filter_by_organization_char1 = filter_by_organization_char1,
                filter_by_first_name = filter_by_first_name,
                filter_by_first_name_char1 = filter_by_first_name_char1,
                filter_by_last_name = filter_by_last_name,
                filter_by_last_name_char1 = filter_by_last_name_char1,
                filter_by_nickname = filter_by_nickname,
                filter_by_nickname_char1 = filter_by_nickname_char1,
                filter_by_street = filter_by_street,
                filter_by_street_char1 = filter_by_street_char1,
                filter_by_postcode = filter_by_postcode,
                filter_by_postcode_char1 = filter_by_postcode_char1,
                filter_by_city = filter_by_city,
                filter_by_city_char1 = filter_by_city_char1,
                filter_by_business_items = filter_by_business_items,
                filter_by_category_items = filter_by_category_items,
                filter_by_tag_items = filter_by_tag_items
            )
        except search.Error as err:
            raise JsonRpcError(
                message = common.format_.safe_errormessage(err),
                code = QUERY_ERROR
            )

        for address in fetched_result["addresses"]:
            addresses.append(address.to_dict(
                include = include,
                exclude = exclude,
                exclude_creation_metadata = exclude_creation_metadata,
                exclude_edit_metadata = exclude_edit_metadata,
                exclude_empty_fields = exclude_empty_fields
            ))

        # Finished
        next_cursor = fetched_result.get("next_cursor")
        if next_cursor:
            next_cursor = next_cursor.web_safe_string


        return dict(
            total_quantity = fetched_result["total_quantity"],
            next_cursor = next_cursor,
            addresses = addresses
        )


    @rpcmethod
    def add_categories(
        self,
        address_keys,
        categories
    ):
        """
        Adds one or more categories to one or more addresses

        ==========
        Parameters
        ==========

        :param address_keys: List with keys or string with one key

        :param categories: List with category names or string with one category
        """

        # Username
        user = cherrypy.request.login

        # Working
        common.addresses.add_categories(
            user = user,
            address_keys = address_keys,
            categories = categories
        )

        # Finished
        return True


    @rpcmethod
    def delete_categories(
        self,
        address_keys,
        categories
    ):
        """
        Deletes one or more categories from one or more addresses

        ==========
        Parameters
        ==========

        :param address_keys: List with keys or string with one key

        :param categories: List with category names or string with one category
        """

        # Username
        user = cherrypy.request.login

        # Working
        common.addresses.add_categories(
            user = user,
            address_keys = address_keys,
            categories = categories
        )

        # Finished
        return True


    @rpcmethod
    def add_tags(
        self,
        address_keys,
        tags
    ):
        """
        Adds one or more tags to one or more addresses

        ==========
        Parameters
        ==========

        :param address_keys: List with keys or string with one key

        :param tags: List with tag names or string with one tag
        """

        # Username
        user = cherrypy.request.login

        # Working
        common.addresses.add_tags(
            user = user,
            address_keys = address_keys,
            tags = tags
        )

        # Finished
        return True


    @rpcmethod
    def delete_tags(
        self,
        address_keys,
        tags
    ):
        """
        Deletes one or more tags from one or more addresses

        ==========
        Parameters
        ==========

        :param address_keys: List with keys or string with one key

        :param tags: List with tag names or string with one tag
        """

        # Username
        user = cherrypy.request.login

        # Working
        common.addresses.add_tags(
            user = user,
            address_keys = address_keys,
            tags = tags
        )

        # Finished
        return True


























jsonrpc = JsonRpc()
jsonrpc.help = jronsrpc_help
jsonrpc.help._cp_config = {"tools.basic_auth.on": False}
jsonrpc.help.exposed = True


