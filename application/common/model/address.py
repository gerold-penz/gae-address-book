#!/usr/bin/env python
# coding: utf-8


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!

import logging
import copy
import datetime
from google.appengine.ext import ndb



def age_years(birthday, basedate = None):
    """
    Gibt das Alter in Jahren zurück.

    Wird kein Basidatum angegeben, dann wird das Alter zum heutigen Tag
    berechnet.
    """

    if not basedate:
        basedate = datetime.date.today()

    years = basedate.year - birthday.year
    months = basedate.month - birthday.month
    days = basedate.day - birthday.day

    if days < 0:
        months -= 1

    if months < 0:
        years -= 1

    return years


class DateTimeSerializable(ndb.Property):

    def _get_for_dict(self, entity):

        value = self._get_value(entity)

        if value:
            return value.isoformat()
        else:
            return value


class DateTimePropertySerializable(ndb.DateTimeProperty, DateTimeSerializable):
    pass


class Tel(ndb.Model):
    label = ndb.StringProperty()
    number = ndb.StringProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Email(ndb.Model):
    label = ndb.StringProperty()
    email = ndb.StringProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Url(ndb.Model):
    label = ndb.StringProperty()
    url = ndb.StringProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Note(ndb.Model):
    text = ndb.TextProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Agreement(ndb.Model):
    text = ndb.TextProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class JournalItem(ndb.Model):
    date_time = ndb.DateTimeProperty()
    text = ndb.TextProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Anniversary(ndb.Model):
    label = ndb.StringProperty(required = True)
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty(required = True, choices = range(1, 13))
    day = ndb.IntegerProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Address(ndb.Model):
    """
    See: https://en.wikipedia.org/wiki/VCard#Properties
    """

    def get_birthday_iso(self):
        """
        Returns the birthday date as ISO string, if possible
        """

        if not self.anniversary_items:
            return

        for anniversary_item in self.anniversary_items:
            assert isinstance(anniversary_item, Anniversary)
            if anniversary_item.label and anniversary_item.label.lower() in [
                u"geburtstag",
                u"birthday"
            ]:
                # Birthday found
                if anniversary_item.year:
                    return u"{year}-{month}-{day}".format(
                        year = anniversary_item.year,
                        month = anniversary_item.month,
                        day = anniversary_item.day
                    )
                else:
                    return u"{month}-{day}".format(
                        month = anniversary_item.month,
                        day = anniversary_item.day
                    )


    def get_age(self):
        """
        Returns the age if possible
        """

        if not self.anniversary_items:
            return

        for anniversary_item in self.anniversary_items:
            assert isinstance(anniversary_item, Anniversary)
            if anniversary_item.label and anniversary_item.label.lower() in [
                u"geburtstag",
                u"birthday"
            ]:
                if anniversary_item.year:
                    # Birthday found
                    birthday = datetime.date(
                        year = anniversary_item.year,
                        month = anniversary_item.month,
                        day = anniversary_item.day
                    )
                    return age_years(birthday)


    uid = ndb.StringProperty(required = True)
    owner = ndb.StringProperty(required = True)

    ct = DateTimePropertySerializable(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = DateTimePropertySerializable(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
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
    journal_items = ndb.StructuredProperty(JournalItem, repeated = True)  # Journaleinträge
    business_items = ndb.StringProperty(repeated = True)  # Branchen
    anniversary_items = ndb.StructuredProperty(Anniversary, repeated = True)  # Jahrestage, Geburtstag
    gender = ndb.StringProperty()
    birthday = ndb.ComputedProperty(get_birthday_iso)
    age = ndb.ComputedProperty(get_age)
    note_items = ndb.StructuredProperty(Note, repeated = True)  # Notizen
    agreement_items = ndb.StructuredProperty(Agreement, repeated = True)  # Vereinbarungen


    def to_dict(
        self,
        include = None,
        exclude = None,
        exclude_creation_metadata = None,
        exclude_edit_metadata = None,
        exclude_empty_fields = None
    ):
        """
        Return address-dict without unneeded fields
        """

        exclude = exclude or []
        if exclude_creation_metadata:
            exclude.extend(["ct", "cu"])
        if exclude_edit_metadata:
            exclude.extend(["et", "eu"])
        exclude = exclude or None

        address_dict = self._to_dict(include = include, exclude = exclude)
        address_dict = copy.deepcopy(address_dict)
        address_dict["key_urlsafe"] = self.key.urlsafe()

        # Repeated fields
        for fieldname in [
            "phone_items",
            "email_items",
            "url_items",
            "note_items",
            "journal_items",
            "anniversary_items",
        ]:
            for field_item in address_dict.get(fieldname, []):
                # Exclude creation metadata
                if exclude_creation_metadata:
                    if "ct" in field_item:
                        del field_item["ct"]
                    if "cu" in field_item:
                        del field_item["cu"]

                # Exclude edit metadata
                if exclude_edit_metadata:
                    if "et" in field_item:
                        del field_item["et"]
                    if "eu" in field_item:
                        del field_item["eu"]

            # Exclude empty fields
            if exclude_empty_fields:
                field = address_dict.get(fieldname, [])
                if not field:
                    del address_dict[fieldname]

        # Exclude empty fields
        if exclude_empty_fields:
            for key, value in address_dict.items():
                if value is None:
                    del address_dict[key]
                elif key in ["category_items", "business_items"]:
                    if not value:
                        del address_dict[key]

        # Finished
        return address_dict


