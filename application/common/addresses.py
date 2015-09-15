#!/usr/bin/env python
# coding: utf-8

import uuid
import authorization
from google.appengine.ext import ndb
from model.address import Address, Tel, Email, Url, Note, JournalItem, Anniversary


def create(
    user,
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
):
    """
    Creates a new Address

    :param user: Username
    :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-*"
    :param category_items: A list of "tags" that can be used to describe the object.
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

            [Note(text = "<note>", ...]

        Example::

            [Note(text = "This is a short note")]


    :param journal_items: A list with JournalItem-objects.
        Syntax::

            [JournalItem(date_time = <datetime.datetime>, text = "<note>"), ...]

        Example::

            [
                JournalItem(
                    date_time = datetime.datetime(2000, 1, 1, 14, 30),
                    text = "This is a short journal item."
                ), ...
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

    :param gender: Defines the person's gender. A single letter.
        M stands for "male",
        F stands for "female",
        O stands for "other",
        N stands for "none or not applicable",
        U stands for "unknown"

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

    # Create address
    address = Address(
        uid = unicode(uuid.uuid4()),
        owner = user,
        cu = user,
        eu = user,
        kind = kind,
    )
    if category_items:
        if isinstance(category_items, basestring):
            category_items = [category_items]
        address.category_items = category_items
    if organization:
        address.organization = organization
    if position:
        address.position = position
    if salutation:
        address.salutation = salutation
    if first_name:
        address.first_name = first_name
    if last_name:
        address.last_name = last_name
    if nickname:
        address.nickname = nickname
    if street:
        address.street = street
    if postcode:
        address.postcode = postcode
    if city:
        address.city = city
    if district:
        address.district = district
    if land:
        address.land = land
    if country:
        address.country = country
    if phone_items:
        for tel in phone_items:
            assert isinstance(tel, Tel)
            if not tel.cu:
                tel.cu = user
            if not tel.eu:
                tel.eu = user
        address.phone_items = phone_items
    if email_items:
        for email in email_items:
            assert isinstance(email, Email)
            if not email.cu:
                email.cu = user
            if not email.eu:
                email.eu = user
        address.email_items = email_items
    if url_items:
        for url in url_items:
            assert isinstance(url, Url)
            if not url.cu:
                url.cu = user
            if not url.eu:
                url.eu = user
        address.url_items = url_items
    if note_items:
        for note in note_items:
            assert isinstance(note, Note)
            if not note.cu:
                note.cu = user
            if not note.eu:
                note.eu = user
        address.note_items = note_items
    if journal_items:
        for journal_item in journal_items:
            assert isinstance(journal_item, JournalItem)
            if not journal_item.cu:
                journal_item.cu = user
            if not journal_item.eu:
                journal_item.eu = user
        address.journal_items = journal_items
    if business_items:
        if isinstance(business_items, basestring):
            business_items = [business_items]
        address.business_items = business_items
    if anniversary_items:
        for anniversary_item in anniversary_items:
            assert isinstance(anniversary_item, Anniversary)
            if not anniversary_item.cu:
                anniversary_item.cu = user
            if not anniversary_item.eu:
                anniversary_item.eu = user
        address.anniversary_items = anniversary_items
    if gender:
        assert gender.lower() in "mfonu"
        address.gender = gender

    # Save
    address.put()

    # Finished
    return address


def get_addresses_count():
    """
    Returns the quantity of addresses in the database
    """

    return Address.query().count()


def get_addresses(page, page_size, order_by = None):
    """
    Returns one page with addresses
    
    :param order_by: List with field names. A minus (-) directly before the
        field name reverts the sort order.

        Possible field names are:
     
        - "uid"
        - "owner"
        - "ct"
        - "cu"
        - "et"
        - "eu"
        - "kind"
        - "category_items"
        - "organization"
        - "position"
        - "salutation"
        - "first_name"
        - "last_name"
        - "nickname"
        - "street"
        - "postcode"
        - "city"
        - "district"
        - "land"
        - "country"
        - "phone_items"
        - "email_items"
        - "url_items"
        - "journal_items"
        - "business_items"
        - "anniversary_items"
        - "gender"
        - "birthday"
        - "age"
        - "note_items"
        - "agreement_items"
    """

    if order_by:
        if isinstance(order_by, basestring):
            order_by = [order_by]

    # Query
    query = Address.query()

    # Sorting
    if order_by:
        order_fields = []
        for order_item in order_by:
            reverse = order_item.startswith("-")
            field_name = order_item.lstrip("-")
            if field_name in Address._properties:
                order_field = Address._properties[field_name]
                if reverse:
                    order_fields.append(-order_field)
                else:
                    order_fields.append(order_field)
        if order_fields:
            query.order(*order_fields)

    # Start with
    offset = (page - 1) * page_size

    # Finished
    return query.fetch(
        offset = offset,
        limit = page_size,
        batch_size = page_size,
        deadline = 30  # seconds
    )


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

