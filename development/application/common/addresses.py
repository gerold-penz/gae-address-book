#!/usr/bin/env python
# coding: utf-8

import uuid
import datetime
import logging
import authorization
import named_values
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import deferred
from bunch import Bunch
from model.address import (
    Address,
    TelItem, EmailItem, UrlItem, NoteItem, JournalItem,
    AgreementItem, FreeDefinedItem, AnniversaryItem
)
from model.address_history import AddressHistory
from model.deleted_address import DeletedAddress
from business_items import add_business_items_to_cache
from category_items import add_category_items_to_cache
from tag_items import add_tag_items_to_cache


ADDRESS_QUANTITY = "address_quantity"


def create(
    user,
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
    Creates a new Address

    :param user: Username
    :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-*"
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

    :param phone_items: A list with Tel-objects.
        Syntax::

            [Tel(label = "<label>", number = "<number">), ...]

        Example::

            [
                Tel(label = "Mobile", number = "+43 123 456 789"),
                Tel(label = "Fax", number = "+43 123 456 999")
            ]

    :param email_items: A list with Email-objects.
        Syntax::

            [Email(label = "<label>", email = "<email>"), ...]

        Example::

            [
                Email(label = "Private", email = "max.mustermann@private.com"),
                Email(label = "Business", email = "m.mustermann@organization.com")
            ]

    :param url_items: A list with Url-objects.
        Syntax::

            [Url(label = "<label>", url = "<url>"), ...]

        Example::

            [Url(label = "Homepage", url = "http://halvar.at/")]

    :param note_items: A list with Note-objects.
        Syntax::

            [NoteItem(text = "<text>", ...]

        Example::

            [NoteItem(text = "This is a short note")]

    :param journal_items: A list with JournalItem-objects.
        Syntax::

            [JournalItem(text = "<text>"), ...]

        Example::

            [JournalItem(text = "This is a short journal item."), ...]

    :param agreement_items: A list with Agreement-objects.
        Syntax::

            [AgreementItem(text = "<text>", ...]

        Example::

            [AgreementItem(text = "This is a short note")]

    :param free_defined_items: A list with FreeDefinedItem-objects.
        Syntax::

            [FreeDefinedItem(label = "<label>", text = "<text>"), ...]

        Example::

            [
                FreeDefinedItem(label = "Shoe-Size", text = "45"),
                FreeDefinedItem(label = "Body-Height", text = "180")
            ]

    :param business_items: A list with business items.
        Example::

            ["carpenter", "furniture"]


    :param anniversary_items: A list with Anniversary-objects.
        Syntax::

            [
                Anniversary(
                    label = "<label>",
                    year = <year>,
                    month = <month [1-12]>,
                    day = <day>
                ), ...
            ]

        Example::

            [Anniversary(label = "Birthday", year = 1974, month = 8, day = 18), ...]

    :param gender: Defines the person's gender. A single lower letter.
        m stands for "male",
        f stands for "female",
        o stands for "other",
        n stands for "none or not applicable",
        u stands for "unknown"

    :return: New created and saved Address-Object

    :rtype: model.address.Address
    """

    # Check authorization
    authorization.check_authorization(user, authorization.ADDRESS_CREATE)

    # Kind
    kind = kind or u"individual"
    assert (
        kind.lower() in (u"individual", u"organization", u"group", u"location") or
        kind.lower().startswith("x-")
    )

    # Now
    utcnow = datetime.datetime.utcnow()

    # Create address
    address = Address(
        uid = unicode(uuid.uuid4()),
        owner = user,
        ct = utcnow,
        cu = user,
        et = utcnow,
        eu = user,
        kind = kind
    )

    # Get data
    if category_items is not None:
        if isinstance(category_items, basestring):
            category_items = [category_items]
        address.category_items = sorted(list(set(category_items)))
    if tag_items is not None:
        if isinstance(tag_items, basestring):
            tag_items = [tag_items]
        address.tag_items = sorted(list(set(tag_items)))
    address.organization = organization
    address.position = position
    address.salutation = salutation
    address.first_name = first_name
    address.last_name = last_name
    address.nickname = nickname
    address.street = street
    address.postcode = postcode
    address.city = city
    address.district = district
    address.land = land
    address.country = country
    if phone_items is not None:
        for tel in phone_items:
            assert isinstance(tel, TelItem)
            tel.uid = unicode(uuid.uuid4())
            tel.ct = utcnow
            tel.cu = user
            tel.et = utcnow
            tel.eu = user
        address.phone_items = phone_items
    if email_items is not None:
        for email in email_items:
            assert isinstance(email, EmailItem)
            email.uid = unicode(uuid.uuid4())
            email.ct = utcnow
            email.cu = user
            email.et = utcnow
            email.eu = user
        address.email_items = email_items
    if url_items is not None:
        for url in url_items:
            assert isinstance(url, UrlItem)
            url.uid = unicode(uuid.uuid4())
            url.ct = utcnow
            url.cu = user
            url.et = utcnow
            url.eu = user
        address.url_items = url_items
    if note_items is not None:
        for note in note_items:
            assert isinstance(note, NoteItem)
            note.uid = unicode(uuid.uuid4())
            note.ct = utcnow
            note.cu = user
            note.et = utcnow
            note.eu = user
        address.note_items = note_items
    if journal_items is not None:
        for journal in journal_items:
            assert isinstance(journal, JournalItem)
            journal.uid = unicode(uuid.uuid4())
            journal.ct = utcnow
            journal.cu = user
            journal.et = utcnow
            journal.eu = user
        address.journal_items = journal_items
    if agreement_items is not None:
        for agreement in agreement_items:
            assert isinstance(agreement, AgreementItem)
            agreement.uid = unicode(uuid.uuid4())
            agreement.ct = utcnow
            agreement.cu = user
            agreement.et = utcnow
            agreement.eu = user
        address.agreement_items = agreement_items
    if free_defined_items is not None:
        for free_defined_item in free_defined_items:
            assert isinstance(free_defined_item, FreeDefinedItem)
            free_defined_item.uid = unicode(uuid.uuid4())
            free_defined_item.ct = utcnow
            free_defined_item.cu = user
            free_defined_item.et = utcnow
            free_defined_item.eu = user
        address.free_defined_items = free_defined_items
    if business_items is not None:
        if isinstance(business_items, basestring):
            business_items = [business_items]
        address.business_items = sorted(list(set(business_items)))
    if anniversary_items is not None:
        for anniversary in anniversary_items:
            assert isinstance(anniversary, AnniversaryItem)
            anniversary.uid = unicode(uuid.uuid4())
            anniversary.ct = utcnow
            anniversary.cu = user
            anniversary.et = utcnow
            anniversary.eu = user
        address.anniversary_items = anniversary_items
    if gender is not None:
        gender = gender.lower()
        assert gender in "mfonu"
        address.gender = gender

    # Save
    address.put()

    # Increment Quantity
    increment_address_quantity_in_cache()

    # Update cached Business-Items
    if address.business_items:
        add_business_items_to_cache(address.business_items)

    # Update cached Category-Items
    if address.category_items:
        add_category_items_to_cache(address.category_items)

    # Update cached Tag-Items
    if address.tag_items:
        add_tag_items_to_cache(address.tag_items)

    # Finished
    return address


# def get_addresses(
#     page,
#     page_size,
#     order_by = None,
#     filter_by_organization = None,
#     filter_by_organization_char1 = None,
#     filter_by_first_name = None,
#     filter_by_first_name_char1 = None,
#     filter_by_last_name = None,
#     filter_by_last_name_char1 = None,
#     filter_by_nickname = None,
#     filter_by_nickname_char1 = None,
#     filter_by_street = None,
#     filter_by_street_char1 = None,
#     filter_by_postcode = None,
#     filter_by_postcode_char1 = None,
#     filter_by_city = None,
#     filter_by_city_char1 = None,
#     filter_by_business_items = None,
#     filter_by_category_items = None,
#     filter_by_tag_items = None
# ):
#     """
#     Returns a dictionary with the count of addresses and one page of addresses
#
#     :param order_by: List with field names. A minus (-) directly before the
#         field name reverts the sort order.
#
#         Possible field names are:
#
#         - "uid"
#         - "owner"
#         - "ct"
#         - "cu"
#         - "et"
#         - "eu"
#         - "kind"
#         - "organization"
#         - "position"
#         - "salutation"
#         - "first_name"
#         - "last_name"
#         - "nickname"
#         - "street"
#         - "postcode"
#         - "city"
#         - "district"
#         - "land"
#         - "country"
#         - "gender"
#         - "birthday"
#         - "age"
#
#     :param filter_by_xxx: Case insensitive filter strings
#
#     :param filter_by_category_items: List with *case sensitive* items.
#
#     :param filter_by_tag_items: List with *case sensitive* items.
#
#     :param filter_by_business_items: List with *case sensitive* items.
#
#     :return: Dictionary with total quantity and one page with addresses::
#
#         {
#             "total_quantity": <Quantity>,
#             "addresses": [<Address>, ...]
#         }
#     """
#
#     if order_by and isinstance(order_by, basestring):
#         order_by = [order_by]
#
#     # Query
#     query = Address.query()
#
#     # Prepare filter and append filter items (strings)
#     filter_items = []
#     if filter_by_organization:
#         filter_items.append(
#             Address.organization_lower == filter_by_organization.strip().lower())
#     if filter_by_organization_char1:
#         filter_items.append(
#             Address.organization_char1 == filter_by_organization_char1[0].lower())
#     if filter_by_first_name:
#         filter_items.append(
#             Address.first_name_lower == filter_by_first_name.strip().lower())
#     if filter_by_first_name_char1:
#         filter_items.append(
#             Address.first_name_char1 == filter_by_first_name_char1[0].lower())
#     if filter_by_last_name:
#         filter_items.append(
#             Address.last_name_lower == filter_by_last_name.strip().lower())
#     if filter_by_last_name_char1:
#         filter_items.append(
#             Address.last_name_char1 == filter_by_last_name_char1[0].lower())
#     if filter_by_nickname:
#         filter_items.append(
#             Address.nickname_lower == filter_by_nickname.strip().lower())
#     if filter_by_nickname_char1:
#         filter_items.append(
#             Address.nickname_char1 == filter_by_nickname_char1[0].lower())
#     if filter_by_street:
#         filter_items.append(
#             Address.street_lower == filter_by_street.strip().lower())
#     if filter_by_street_char1:
#         filter_items.append(
#             Address.street_char1 == filter_by_street_char1[0].lower())
#     if filter_by_postcode:
#         filter_items.append(
#             Address.postcode_lower == filter_by_postcode.strip().lower())
#     if filter_by_postcode_char1:
#         filter_items.append(
#             Address.postcode_char1 == filter_by_postcode_char1[0].lower())
#     if filter_by_city:
#         filter_items.append(
#             Address.city_lower == filter_by_city.strip().lower())
#     if filter_by_city_char1:
#         filter_items.append(
#             Address.city_char1 == filter_by_city_char1[0].lower())
#
#     # Append filter items (lists) --> IN
#     if filter_by_business_items:
#         if isinstance(filter_by_business_items, basestring):
#             filter_by_business_items = [filter_by_business_items]
#         for business_item in filter_by_business_items:
#             filter_items.append(Address.business_items == business_item)
#     if filter_by_category_items:
#         if isinstance(filter_by_category_items, basestring):
#             filter_by_category_items = [filter_by_category_items]
#         for category_item in filter_by_category_items:
#             filter_items.append(Address.category_items == category_item)
#     if filter_by_tag_items:
#         if isinstance(filter_by_tag_items, basestring):
#             filter_by_tag_items = [filter_by_tag_items]
#         for tag_item in filter_by_tag_items:
#             filter_items.append(Address.tag_items == tag_item)
#
#     # Filter query
#     query = query.filter(*filter_items)
#
#     # Sorting
#     if order_by:
#         order_fields = []
#         for order_item in order_by:
#             # Parse
#             reverse = order_item.startswith("-")
#             field_name = order_item.lstrip("-")
#
#             # Check field name
#             if "%s_lower" % field_name in Address._properties:
#                 order_field = Address._properties["%s_lower" % field_name]
#             elif field_name in Address._properties:
#                 order_field = Address._properties[field_name]
#             else:
#                 continue
#
#             # Add sort order
#             if reverse:
#                 order_fields.append(-order_field)
#             else:
#                 order_fields.append(order_field)
#
#         # Sort query
#         if order_fields:
#             query = query.order(*order_fields)
#
#     # Start with
#     offset = (page - 1) * page_size
#
#     # Fetch adresses
#     addresses = query.fetch(
#         offset = offset,
#         limit = page_size,
#         batch_size = page_size,
#         deadline = 30  # seconds
#     )
#
#     # Quantity
#     if not filter_items:
#         quantity = get_address_quantity_cached()
#     else:
#         quantity = query.count()
#
#     # Finished
#     return dict(
#         total_quantity = quantity,
#         addresses = addresses
#     )


def get_address(key_urlsafe = None, address_uid = None):
    """
    Returns one address
    """

    assert key_urlsafe or address_uid

    if key_urlsafe:
        key = ndb.Key(urlsafe = key_urlsafe)
        return key.get(deadline = 30)
    else:
        addresses = Address.query(Address.uid == address_uid).fetch(
            deadline = 30  # seconds
        )
        if addresses:
            return addresses[0]


def save_address(
    user,
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

    The original address will saved before into the *address_history*-table.

    :param user: Username
    :param owner: Username of the owner
    :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-*"
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

    :param phone_items: A list with Tel-objects.
        Syntax::

            [Tel(label = "<label>", number = "<number">), ...]

        Example::

            [
                Tel(label = "Mobile", number = "+43 123 456 789"),
                Tel(label = "Fax", number = "+43 123 456 999")
            ]

    :param email_items: A list with Email-objects.
        Syntax::

            [Email(label = "<label>", email = "<email>"), ...]

        Example::

            [
                Email(label = "Private", email = "max.mustermann@private.com"),
                Email(label = "Business", email = "m.mustermann@organization.com")
            ]

    :param url_items: A list with Url-objects.
        Syntax::

            [Url(label = "<label>", url = "<url>"), ...]

        Example::

            [Url(label = "Homepage", url = "http://halvar.at/")]

    :param note_items: A list with Note-objects.
        Syntax::

            [NoteItem(text = "<text>", ...]

        Example::

            [NoteItem(text = "This is a short note")]

    :param journal_items: A list with JournalItem-objects.
        Syntax::

            [JournalItem(text = "<text>"), ...]

        Example::

            [JournalItem(text = "This is a short journal item."), ...]

    :param agreement_items: A list with Agreement-objects.
        Syntax::

            [AgreementItem(text = "<text>", ...]

        Example::

            [AgreementItem(text = "This is a short note")]

    :param free_defined_items: A list with FreeDefinedItem-objects.
        Syntax::

            [FreeDefinedItem(label = "<label>", text = "<text>"), ...]

        Example::

            [
                FreeDefinedItem(label = "Shoe-Size", text = "45"),
                FreeDefinedItem(label = "Body-Height", text = "180")
            ]

    :param business_items: A list with strings.
        Example::

            ["carpenter", "furniture"]


    :param anniversary_items: A list with Anniversary-objects.
        Syntax::

            [
                Anniversary(
                    label = "<label>",
                    year = <year>,
                    month = <month [1-12]>,
                    day = <day>
                ), ...
            ]

        Example::

            [Anniversary(label = "Birthday", year = 1974, month = 8, day = 18), ...]

    :param gender: Defines the person's gender. A single lower letter.
        m stands for "male",
        f stands for "female",
        o stands for "other",
        n stands for "none or not applicable",
        u stands for "unknown"

    :return: Edited Address-Object

    :rtype: model.address.Address
    """

    assert key_urlsafe or address_uid

    # Load original address
    address = get_address(key_urlsafe = key_urlsafe, address_uid = address_uid)

    # Check authorization
    if address.owner == user:
        authorization.check_authorization(user, authorization.OWN_ADDRESS_EDIT)
    else:
        authorization.check_authorization(user, authorization.PUBLIC_ADDRESS_EDIT)

    # Save original address to *address_history*.
    address_history = AddressHistory(
        parent = address.key,
        cu = user,
        address_dict = address.to_dict()
    )
    address_history.put()

    # Now
    utcnow = datetime.datetime.utcnow()

    # Change *et* and *eu*
    address.et = utcnow
    address.eu = user

    # Check arguments and set values
    if owner is not None:
        address.owner = owner
    if kind is not None:
        kind = kind.lower()
        assert (
            kind in (u"individual", u"organization", u"group", u"location") or
            kind.startswith("x-")
        )
        address.kind = kind
    if category_items is not None:
        if isinstance(category_items, basestring):
            category_items = [category_items]
        address.category_items = sorted(list(set(category_items)))
    if tag_items is not None:
        if isinstance(tag_items, basestring):
            tag_items = [tag_items]
        address.tag_items = sorted(list(set(tag_items)))
    if organization is not None:
        address.organization = organization
    if position is not None:
        address.position = position
    if salutation is not None:
        address.salutation = salutation
    if first_name is not None:
        address.first_name = first_name
    if last_name is not None:
        address.last_name = last_name
    if nickname is not None:
        address.nickname = nickname
    if street is not None:
        address.street = street
    if postcode is not None:
        address.postcode = postcode
    if city is not None:
        address.city = city
    if district is not None:
        address.district = district
    if land is not None:
        address.land = land
    if country is not None:
        address.country = country
    if phone_items is not None:
        for tel in phone_items:
            assert isinstance(tel, TelItem)
            if tel.uid:
                for old_tel in address.phone_items:
                    if old_tel.uid == tel.uid:
                        tel.ct = old_tel.ct
                        tel.cu = old_tel.cu
                        tel.et = old_tel.et
                        tel.eu = old_tel.eu
                        if (
                            old_tel.label != tel.label or
                            old_tel.number != tel.number
                        ):
                            tel.et = utcnow
                            tel.eu = user
            else:
                tel.uid = unicode(uuid.uuid4())
            if not tel.ct:
                tel.ct = utcnow
            if not tel.cu:
                tel.cu = user
            if not tel.et:
                tel.et = utcnow
            if not tel.eu:
                tel.eu = user
        address.phone_items = [
            phone_item for phone_item in phone_items if phone_item.number
        ]
    if email_items is not None:
        for email in email_items:
            assert isinstance(email, EmailItem)
            if email.uid:
                for old_email in address.email_items:
                    if old_email.uid == email.uid:
                        email.ct = old_email.ct
                        email.cu = old_email.cu
                        email.et = old_email.et
                        email.eu = old_email.eu
                        if (
                            old_email.label != email.label or
                            old_email.email != email.email
                        ):
                            email.et = utcnow
                            email.eu = user
            else:
                email.uid = unicode(uuid.uuid4())
            if not email.ct:
                email.ct = utcnow
            if not email.cu:
                email.cu = user
            if not email.et:
                email.et = utcnow
            if not email.eu:
                email.eu = user
        address.email_items = [
            email_item for email_item in email_items if email_item.email
        ]
    if url_items is not None:
        for url in url_items:
            assert isinstance(url, UrlItem)
            if url.uid:
                for old_url in address.url_items:
                    if old_url.uid == url.uid:
                        url.ct = old_url.ct
                        url.cu = old_url.cu
                        url.et = old_url.et
                        url.eu = old_url.eu
                        if (
                            old_url.label != url.label or
                            old_url.url != url.url
                        ):
                            url.et = utcnow
                            url.eu = user
            else:
                url.uid = unicode(uuid.uuid4())
            if not url.ct:
                url.ct = utcnow
            if not url.cu:
                url.cu = user
            if not url.et:
                url.et = utcnow
            if not url.eu:
                url.eu = user

            # Mit "http" ergänzen
            if url.url:
                url.url = url.url.strip()
                if not url.url.startswith("http"):
                    url.url = u"http://" + url.url

        address.url_items = [
            url_item for url_item in url_items if url_item.url
        ]

    if note_items is not None:
        for note in note_items:
            assert isinstance(note, NoteItem)
            if note.uid:
                for old_note in address.note_items:
                    if old_note.uid == note.uid:
                        note.ct = old_note.ct
                        note.cu = old_note.cu
                        note.et = old_note.et
                        note.eu = old_note.eu
                        if old_note.text != note.text:
                            note.et = utcnow
                            note.eu = user
            else:
                note.uid = unicode(uuid.uuid4())
            if not note.ct:
                note.ct = utcnow
            if not note.cu:
                note.cu = user
            if not note.et:
                note.et = utcnow
            if not note.eu:
                note.eu = user
        address.note_items = [
            note_item for note_item in note_items if note_item.text
        ]
    if journal_items is not None:
        for journal in journal_items:
            assert isinstance(journal, JournalItem)
            if journal.uid:
                for old_journal in address.journal_items:
                    if old_journal.uid == journal.uid:
                        journal.ct = old_journal.ct
                        journal.cu = old_journal.cu
                        journal.et = old_journal.et
                        journal.eu = old_journal.eu
                        if old_journal.text != journal.text:
                            journal.et = utcnow
                            journal.eu = user
            else:
                journal.uid = unicode(uuid.uuid4())
            if not journal.ct:
                journal.ct = utcnow
            if not journal.cu:
                journal.cu = user
            if not journal.et:
                journal.et = utcnow
            if not journal.eu:
                journal.eu = user
        address.journal_items = [
            journal_item for journal_item in journal_items if journal_item.text
        ]
    if agreement_items is not None:
        for agreement in agreement_items:
            assert isinstance(agreement, AgreementItem)
            if agreement.uid:
                for old_agreement in address.agreement_items:
                    if old_agreement.uid == agreement.uid:
                        agreement.ct = old_agreement.ct
                        agreement.cu = old_agreement.cu
                        agreement.et = old_agreement.et
                        agreement.eu = old_agreement.eu
                        if old_agreement.text != agreement.text:
                            agreement.et = utcnow
                            agreement.eu = user
            else:
                agreement.uid = unicode(uuid.uuid4())
            if not agreement.ct:
                agreement.ct = utcnow
            if not agreement.cu:
                agreement.cu = user
            if not agreement.et:
                agreement.et = utcnow
            if not agreement.eu:
                agreement.eu = user
        address.agreement_items = [
            agreement_item for agreement_item in agreement_items if agreement_item.text
        ]
    if free_defined_items is not None:
        for free_defined_item in free_defined_items:
            assert isinstance(free_defined_item, FreeDefinedItem)
            if free_defined_item.uid:
                for old_free_defined in address.free_defined_items:
                    if old_free_defined.uid == free_defined_item.uid:
                        free_defined_item.ct = old_free_defined.ct
                        free_defined_item.cu = old_free_defined.cu
                        free_defined_item.et = old_free_defined.et
                        free_defined_item.eu = old_free_defined.eu
                        if old_free_defined.text != free_defined_item.text:
                            free_defined_item.et = utcnow
                            free_defined_item.eu = user
            else:
                free_defined_item.uid = unicode(uuid.uuid4())
            if not free_defined_item.ct:
                free_defined_item.ct = utcnow
            if not free_defined_item.cu:
                free_defined_item.cu = user
            if not free_defined_item.et:
                free_defined_item.et = utcnow
            if not free_defined_item.eu:
                free_defined_item.eu = user
        address.free_defined_items = [
            free_defined_item for free_defined_item in free_defined_items if free_defined_item.text
        ]
    if business_items is not None:
        if isinstance(business_items, basestring):
            business_items = [business_items]
        address.business_items = sorted(list(set(business_items)))
    if anniversary_items is not None:
        for anniversary in anniversary_items:
            assert isinstance(anniversary, AnniversaryItem)
            if anniversary.uid:
                for old_anniversary in address.anniversary_items:
                    if old_anniversary.uid == anniversary.uid:
                        anniversary.ct = old_anniversary.ct
                        anniversary.cu = old_anniversary.cu
                        anniversary.et = old_anniversary.et
                        anniversary.eu = old_anniversary.eu
                        if (
                            old_anniversary.label != anniversary.label or
                            old_anniversary.year != anniversary.year or
                            old_anniversary.month != anniversary.month or
                            old_anniversary.day != anniversary.day
                        ):
                            anniversary.et = utcnow
                            anniversary.eu = user
            else:
                anniversary.uid = unicode(uuid.uuid4())
            if not anniversary.ct:
                anniversary.ct = utcnow
            if not anniversary.cu:
                anniversary.cu = user
            if not anniversary.et:
                anniversary.et = utcnow
            if not anniversary.eu:
                anniversary.eu = user
        address.anniversary_items = [
            anniversary_item for anniversary_item in anniversary_items if
            anniversary_item.year or anniversary_item.month or anniversary_item.day
        ]
    if gender is not None:
        gender = gender.lower()
        assert gender in "mfonu"
        address.gender = gender

    # save changes
    address.put()

    # Return saved address
    return address


def delete_all_search_indexes():
    """
    Deletes all documents in the "Address" search index
    """

    logging.info(u"delete_all_search_indexes: BEGIN")

    index = search.Index("Address")
    while True:
        document_ids = [
            document.doc_id for document in
            index.get_range(limit = 200, ids_only = True)
        ]
        if not document_ids:
            break
        index.delete(document_ids)

    logging.info(u"delete_all_search_indexes: END")


def start_delete_all_search_indexes():
    """
    Starts the deletion of all search indexes deferred
    """

    deferred.defer(delete_all_search_indexes)


def start_refresh_index():
    """
    Loads every Address and saves it again.
    """

    # Start helper function with deferred
    deferred.defer(_refresh_index)


def _refresh_index():
    """
    This function will started by defered
    """

    # Delete full search index
    delete_all_search_indexes()

    # Resave all addresses
    logging.info(u"refresh_indexes: BEGIN")

    query = Address().query()
    for address in query.iter(batch_size = 200):
        address.put()

    logging.info(u"refresh_indexes: END")


def search_addresses(
    query_string,
    page,
    page_size = 20,
    returned_fields = None
):
    """
    Searches for addresses in the "Address" index

    :param query_string: Search string

    :param page: Page number

    :param page_size: Page size

    :returned_fields: Field names of the result.
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
        - category
        - tag
        - business
        - phone
        - email
        - url
        - note
        - journal
        - agreement
        - anniversary
    """

    index = search.Index("Address")
    offset = (page - 1) * page_size

    if not returned_fields:
        returned_fields = [
            "organization",
            "first_name",
            "last_name"
        ]

    query_options = search.QueryOptions(
        limit = page_size,
        offset = offset,
        returned_fields = returned_fields
    )

    # Search
    query = search.Query(query_string = query_string, options = query_options)
    result = index.search(query)

    # Finished
    return result


def delete_address(user, key_urlsafe = None, address_uid = None, force = False):
    """
    Deletes one address

    :param user: Username

    :param force: If `True`, address will deleted full.
        Else, the address will moved into the DeleteAddress model.
    """

    assert key_urlsafe or address_uid

    if force and key_urlsafe:
        address = None
        key = ndb.Key(urlsafe = key_urlsafe)
    else:
        # Load address
        address = get_address(
            key_urlsafe = key_urlsafe,
            address_uid = address_uid
        )
        key = address.key

    if force:
        # Delete address-history items
        history_keys = []
        for history_key in AddressHistory.query(ancestor = key).iter(keys_only = True):
            history_keys.append(history_key)
        ndb.delete_multi(history_keys)
    else:
        # Copy address to *DeletedAddress-Model*.
        deleted_address = DeletedAddress(
            du = user,
            address_dict = address.to_dict()
        )
        deleted_address.put()

    # Delete address
    key.delete()

    # Decrement Quantity
    decrement_address_quantity_in_cache()


def delete_all_addresses(yes_do_it = False):
    """
    Deletes really ALL addresses and search_indexes
    """

    if not yes_do_it:
        return

    logging.info(u"delete_all_addresses: BEGIN")
    
    # Delete addresses
    address_keys = []
    for index, key in enumerate(Address.query().iter(keys_only = True)):
        address_keys.append(key)
        ndb.delete_multi(address_keys)
        if index % 100:
            address_keys = []

    # Delete address histories
    address_history_keys = []
    for index, key in enumerate(AddressHistory.query().iter(keys_only = True)):
        address_history_keys.append(key)
        ndb.delete_multi(address_history_keys)
        if index % 100:
            address_history_keys = []

    logging.info(u"delete_all_addresses: END")


def start_delete_all_addresses(yes_do_it = False):
    """
    Starts the deletion of all addresses deferred
    """

    deferred.defer(delete_all_addresses, yes_do_it = yes_do_it)


def get_address_quantity_direct():
    """
    Returns the quantity of undeleted addresses in the database.
    Directly from the Address model.
    """

    return Address.query().count()


def get_address_quantity_cached():
    """
    Returns all used category items as set.
    """

    # Cache get
    address_quantity = named_values.get_value(name = ADDRESS_QUANTITY)
    if address_quantity is not None:
        return address_quantity

    # Fetch quantity direct from the Address model
    address_quantity = get_address_quantity_direct()

    # Cache set
    named_values.set_value(name = ADDRESS_QUANTITY, value = address_quantity)

    # Finished
    return address_quantity


def update_address_quantity_cache():
    """
    Updates the "address_quantity" NamedValue entity
    """

    # Cache set
    named_values.set_value(name = ADDRESS_QUANTITY, value = get_address_quantity_direct())


def increment_address_quantity_in_cache():
    """
    Increments address quantity in the cache
    """

    named_values.increment(name = ADDRESS_QUANTITY)


def decrement_address_quantity_in_cache():
    """
    Decrements address quantity in the cache
    """

    named_values.decrement(name = ADDRESS_QUANTITY)


def update_address_search_index():
    """
    Updates all documents in the "Address" search index
    """

    index = search.Index("Address")
    address_keys = set()

    # Iterate over all addresses
    for address in Address.query().iter(batch_size = 200):

        # Append key
        address_keys.add(address.key.urlsafe())

        # Update search index for the address
        address.update_search_index()

    # Fetch all document ids
    document_ids = set()
    start_id = None
    while True:

        fetched_document_ids = index.get_range(
            start_id = start_id,
            include_start_object = False,
            limit = 200,
            ids_only = True
        )
        if not fetched_document_ids:
            break

        for document in fetched_document_ids:
            document_ids.add(document.doc_id)

        start_id = fetched_document_ids[-1].doc_id

    # Delete search indexes for not existing addresses
    for document_id in document_ids:
        if document_id not in address_keys:
            index.delete(document_id)


def get_addresses_by_search(
    page,
    page_size,
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
    :return: Dictionary with total quantity and one page with 
        real addresses::

            {
                "total_quantity": <Quantity>,
                "addresses": [<Address>, ...]
            }
            
        Address-Fields:

        - key_urlsafe
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
        - immoads_makler_id
        
    """

    index = search.Index("Address")
    offset = (page - 1) * page_size

    # Sorting
    if order_by and isinstance(order_by, basestring):
        order_by = [order_by]
    if order_by:
        sort_expressions = []
        for order_item in order_by:
            # Parse
            field_name = order_item.lstrip("-").lower()
            if order_item.startswith("-"):
                direction = search.SortExpression.DESCENDING
            else:
                direction = search.SortExpression.ASCENDING

            sort_expressions.append(
                search.SortExpression(
                    expression = field_name,
                    direction = direction
                )
            )
        sort_options = search.SortOptions(
            expressions = sort_expressions,
            limit = search.MAXIMUM_SORTED_DOCUMENTS
        )
    else:
        sort_options = None

    # Query Options
    query_options = search.QueryOptions(
        limit = page_size,
        offset = offset,
        sort_options = sort_options,
        ids_only = True
    )

    # Query String
    if not query_string:
        query_string = u""

    if filter_by_organization:
        query_string += u' organization:%s' % filter_by_organization
    if filter_by_organization_char1:
        query_string += u' organization_char1:%s' % filter_by_organization_char1[0]
    if filter_by_first_name:
        query_string += u' first_name:%s' % filter_by_first_name
    if filter_by_first_name_char1:
        query_string += u' first_name_char1:%s' % filter_by_first_name_char1[0]
    if filter_by_last_name:
        query_string += u' last_name:%s' % filter_by_last_name
    if filter_by_last_name_char1:
        query_string += u' last_name_char1:%s' % filter_by_last_name_char1[0]
    if filter_by_nickname:
        query_string += u' nickname:%s' % filter_by_nickname
    if filter_by_nickname_char1:
        query_string += u' nickname_char1:%s' % filter_by_nickname_char1[0]
    if filter_by_street:
        query_string += u' street:%s' % filter_by_street
    if filter_by_street_char1:
        query_string += u' street_char1:%s' % filter_by_street_char1[0]
    if filter_by_postcode:
        query_string += u' postcode:%s' % filter_by_postcode
    if filter_by_postcode_char1:
        query_string += u' postcode_char1:%s' % filter_by_postcode_char1[0]
    if filter_by_city:
        query_string += u' city:%s' % filter_by_city
    if filter_by_city_char1:
        query_string += u' city_char1:%s' % filter_by_city_char1[0]
    if filter_by_business_items:
        if isinstance(filter_by_business_items, basestring):
            filter_by_business_items = [filter_by_business_items]
        for business_item in filter_by_business_items:
            query_string += u' business:"%s"' % business_item
    if filter_by_category_items:
        if isinstance(filter_by_category_items, basestring):
            filter_by_category_items = [filter_by_category_items]
        for category_item in filter_by_category_items:
            query_string += u' category:"%s"' % category_item
    if filter_by_tag_items:
        if isinstance(filter_by_tag_items, basestring):
            filter_by_tag_items = [filter_by_tag_items]
        for tag_item in filter_by_tag_items:
            query_string += u' tag:"%s"' % tag_item

    query_string = query_string.lstrip()

    # Search
    query = search.Query(query_string = query_string, options = query_options)
    search_result = index.search(query)

    # Fetch addresses
    addresses = []
    for document in search_result.results:
        key_urlsafe = document.doc_id
        key = ndb.Key(urlsafe = key_urlsafe)
        address = key.get()
        if address:
            addresses.append(address)

    # Finished
    return {
        "total_quantity": search_result.number_found,
        "addresses": addresses
    }

