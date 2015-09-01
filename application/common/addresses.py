#!/usr/bin/env python
# coding: utf-8

import uuid
import model.address


def create(
    user,
    kind = None,
    categories = None,
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


    # ToDo: Hier gehts weiter

):
    """
    Creates a new Address

    :return: New created Address-Object

    :param user: Username
    :param kind: "application" | "individual" | "group" | "location" | "organization" | "x-*"
    :param categories: A list of "tags" that can be used to describe the object.
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


    :rtype: model.address.Address
    """

    # Parameters
    kind = kind or u"individual"
    assert (
        kind.lower() in (u"individual", u"organization", u"group", u"location") or
        kind.lower().startswith("x-")
    )
    if isinstance(categories, basestring):
        categories = [categories]

    # Create address
    address = model.address.Address(
        uid = unicode(uuid.uuid4()),
        owner = user,
        creation_user = user,
        edit_user = user,
        kind = kind,
        categories = categories,
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
        # land = ndb.StringProperty()  # Bundesland
        # country = ndb.StringProperty()  # Land
        # phone_numbers = ndb.StructuredProperty(Tel)  # Telefonnummern
        # email_addresses = ndb.StructuredProperty(Email)  # E-Mail-Adressen
        # web_urls = ndb.StructuredProperty(Url)  # URLs
        # notes = ndb.StructuredProperty(Note)  # Notizen
        # journal = ndb.StructuredProperty(Journal)  # Journaleinträge
        # business = ndb.StringProperty(repeated = True)  # Branchen
        # anniversaries = ndb.StructuredProperty(Date)  # Jahrestage, Geburtstag
        # gender = ndb.StringProperty(verbose_name = u"VCard: GENDER")
    )

    # Save
    address.put()

    # Finished
    return address
