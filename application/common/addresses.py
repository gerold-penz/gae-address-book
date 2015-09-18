#!/usr/bin/env python
# coding: utf-8

import uuid
import logging
import datetime
import authorization
from google.appengine.ext import ndb
from model.address import Address, Tel, Email, Url, Note, JournalItem, Anniversary
from model.address_history import AddressHistory


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
        address.category_items = sorted(list(set(category_items)))
    if tag_items:
        if isinstance(tag_items, basestring):
            tag_items = [tag_items]
        address.tag_items = sorted(list(set(tag_items)))
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
        address.business_items = sorted(list(set(business_items)))
    if anniversary_items:
        for anniversary_item in anniversary_items:
            assert isinstance(anniversary_item, Anniversary)
            if not anniversary_item.cu:
                anniversary_item.cu = user
            if not anniversary_item.eu:
                anniversary_item.eu = user
        address.anniversary_items = anniversary_items
    if gender:
        gender = gender.lower()
        assert gender in "mfonu"
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


def get_addresses(
    page,
    page_size,
    order_by = None,
    filter_by_organization = None,
    filter_by_first_name = None,
    filter_by_last_name = None,
    filter_by_postcode = None,
    filter_by_city = None,
    filter_by_category_items = None,
    filter_by_tag_items = None,
    filter_by_business_items = None
):
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
        - "gender"
        - "birthday"
        - "age"

    :param filter_by_xxx: Case insensitive filter strings

    :param filter_by_category_items: List with *case sensitive* items.

    :param filter_by_tag_items: List with *case sensitive* items.

    :param filter_by_business_items: List with *case sensitive* items.
    """

    if order_by and isinstance(order_by, basestring):
        order_by = [order_by]

    # Query
    query = Address.query()

    # Prepare filter
    filter_items = []

    # Append filter items (strings)
    if filter_by_organization:
        filter_items.append(Address.organization_lower == filter_by_organization.strip().lower())
    if filter_by_first_name:
        filter_items.append(Address.first_name_lower == filter_by_first_name.strip().lower())
    if filter_by_last_name:
        filter_items.append(Address.last_name_lower == filter_by_last_name.strip().lower())
    if filter_by_postcode:
        filter_items.append(Address.postcode_lower == filter_by_postcode.strip().lower())
    if filter_by_city:
        filter_items.append(Address.city_lower == filter_by_city.strip().lower())

    # Append filter items (lists) --> IN
    if filter_by_category_items:
        if isinstance(filter_by_category_items, basestring):
            filter_by_category_items = [filter_by_category_items]
        for category_item in filter_by_category_items:
            filter_items.append(Address.category_items == category_item)
    if filter_by_tag_items:
        if isinstance(filter_by_tag_items, basestring):
            filter_by_tag_items = [filter_by_tag_items]
        for tag_item in filter_by_tag_items:
            filter_items.append(Address.tag_items == tag_item)
    if filter_by_business_items:
        if isinstance(filter_by_business_items, basestring):
            filter_by_business_items = [filter_by_business_items]
        for business_item in filter_by_business_items:
            filter_items.append(Address.business_items == business_item)

    # Filter query
    query = query.filter(*filter_items)

    # Sorting
    if order_by:
        order_fields = []
        for order_item in order_by:
            # Parse
            reverse = order_item.startswith("-")
            field_name = order_item.lstrip("-")

            # Check field name
            if "%s_lower" % field_name in Address._properties:
                order_field = Address._properties["%s_lower" % field_name]
            elif field_name in Address._properties:
                order_field = Address._properties[field_name]
            else:
                continue

            # Add sort order
            if reverse:
                order_fields.append(-order_field)
            else:
                order_fields.append(order_field)

        # Sort query
        if order_fields:
            query = query.order(*order_fields)

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



def save_address(user, key_urlsafe = None, address_uid = None, address_data = None):
    """
    Saves one address

    The original address will saved before into the *address_history*-table.

    :param address_data: Dictionary with fields to change. If one field doesn't
        exist, the value will not be changed. If one filed exists and has no
        content, the original content will erased.
    """

    assert key_urlsafe or address_uid
    assert address_data

    # Load original address
    address = get_address(key_urlsafe = key_urlsafe, address_uid = address_uid)

    # Save original address to *address_history*.
    address_history = AddressHistory(
        address_key = address.key(),
        address_dict = address.to_dict()
    )
    address_history.put()

    # Change *et* and *eu*
    address.et = datetime.datetime.now()
    address.eu = user

    # Change field-values
    for key, value in address_data.items():

        # Read only fields
        if key in ["key", "uid", "owner", "ct", "cu", "et", "eu"]:
            continue

        # Change
        address[key] = value

    # save changes
    address.put()

    # Return saved address
    return address


def get_categories():
    """
    Returns all used categorie-names as set.
    """

    categories = set()

    query = Address.query(projection = [Address.category_items], distinct = True)
    for address in query.iter(batch_size = 1000):
        for category_item in address.category_items:
            categories.add(category_item)

    # Finished
    return categories








