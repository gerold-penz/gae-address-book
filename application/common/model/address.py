#!/usr/bin/env python
# coding: utf-8


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


from google.appengine.ext import ndb


class Tel(ndb.Model):
    label = ndb.StringProperty()
    number = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Email(ndb.Model):
    label = ndb.StringProperty()
    email = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Url(ndb.Model):
    label = ndb.StringProperty()
    url = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Note(ndb.Model):
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Agreement(ndb.Model):
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class JournalItem(ndb.Model):
    date_time = ndb.DateTimeProperty()
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Anniversary(ndb.Model):
    label = ndb.StringProperty(required = True)
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty(required = True, choices = range(1, 13))
    day = ndb.IntegerProperty(required = True)

    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Address(ndb.Model):
    """
    See: https://en.wikipedia.org/wiki/VCard#Properties
    """

    uid = ndb.StringProperty(required = True)
    owner = ndb.StringProperty(required = True)
    ct = ndb.DateTimeProperty(auto_now_add = True, required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(auto_now = True, required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")

    kind = ndb.StringProperty(required = True)
    category_items = ndb.StringProperty(repeated = True)
    organization = ndb.StringProperty()
    position = ndb.StringProperty()
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
    phone_items = ndb.StructuredProperty(Tel, repeated = True)  # Telefonnummern
    email_items = ndb.StructuredProperty(Email, repeated = True)  # E-Mail-Adressen
    url_items = ndb.StructuredProperty(Url, repeated = True)  # URLs
    note_items = ndb.StructuredProperty(Note, repeated = True)  # Notizen
    journal_items = ndb.StructuredProperty(JournalItem, repeated = True)  # Journaleinträge
    business_items = ndb.StringProperty(repeated = True)  # Branchen
    anniversary_items = ndb.StructuredProperty(Anniversary, repeated = True)  # Jahrestage, Geburtstag
    gender = ndb.StringProperty()



