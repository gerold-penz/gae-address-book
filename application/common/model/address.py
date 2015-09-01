#!/usr/bin/env python
# coding: utf-8


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


from google.appengine.ext import ndb


class Address(ndb.Model):
    """
    See: https://en.wikipedia.org/wiki/VCard#Properties
    """

    uid = ndb.StringProperty(verbose_name = u"VCard: UID")
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    kind = ndb.StringProperty(
        choices = [u"individual", u"organization", u"group", u"location"],
        default = u"individual",
        verbose_name = u"VCard: KIND"
    )
    categories = ndb.StringProperty(repeated = True, verbose_name = u"VCard: CATEGORIES")
    source = ndb.StringProperty(verbose_name = u"VCard: SOURCE")
    company = ndb.StringProperty(verbose_name = u"VCard: ORG")
    role = ndb.StringProperty(verbose_name = u"VCard: ROLE")
    salutation = ndb.StringProperty()  # Anrede/Titel
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    nickname = ndb.StringProperty()
    street = ndb.StringProperty()
    postcode = ndb.StringProperty()
    city = ndb.StringProperty()
    district = ndb.StringProperty()  # Bezirk
    land = ndb.StringProperty()  # Bundesland
    country = ndb.StringProperty()  # Land
    phone_numbers = ndb.StructuredProperty(Tel)  # Telefonnummern
    email_addresses = ndb.StructuredProperty(Email)  # E-Mail-Adressen
    web_urls = ndb.StructuredProperty(Url)  # URLs
    notes = ndb.StructuredProperty(Note)  # Notizen
    journal = ndb.StructuredProperty(Journal)  # Journaleinträge
    business = ndb.StringProperty(repeated = True)  # Branchen
    anniversaries = ndb.StructuredProperty(Date)  # Jahrestage, Geburtstag
    gender = ndb.StringProperty(verbose_name = u"VCard: GENDER")


class Tel(ndb.Model):
    name = ndb.StringProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    number = ndb.StringProperty()


class Email(ndb.Model):
    name = ndb.StringProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    address = ndb.StringProperty()


class Url(ndb.Model):
    name = ndb.StringProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    url = ndb.StringProperty()


class Note(ndb.Model):
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    note = ndb.TextProperty()


class Agreement(ndb.Model):
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    note = ndb.TextProperty()


class Journal(ndb.Model):
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    note = ndb.TextProperty()


class Date(ndb.Model):
    user = ndb.StringProperty()
    creation_timestamp = ndb.DateTimeProperty(auto_now_add = True)
    creation_user = ndb.StringProperty()
    edit_timestamp = ndb.DateTimeProperty(auto_now = True)
    edit_user = ndb.StringProperty()
    date = ndb.DateProperty()


