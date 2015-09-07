#!/usr/bin/env python
# coding: utf-8


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!

import copy
from google.appengine.ext import ndb


class DateTimePropertySerializable(ndb.DateTimeProperty):

    def _get_for_dict(self, entity):
        """Retrieve the value like _get_value(), processed for _to_dict().

        Property subclasses can override this if they want the dictionary
        returned by entity._to_dict() to contain a different value.  The
        main use case is StructuredProperty and LocalStructuredProperty.

        NOTES:

        - If you override _get_for_dict() to return a different type, you
          must override _validate() to accept values of that type and
          convert them back to the original type.

        - If you override _get_for_dict(), you must handle repeated values
          and None correctly.  (See _StructuredGetForDictMixin for an
          example.)  However, _validate() does not need to handle these.
        """

        value = self._get_value(entity)

        if value:
            return value.isoformat()
        else:
            return value


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
    note_items = ndb.StructuredProperty(Note, repeated = True)  # Notizen
    journal_items = ndb.StructuredProperty(JournalItem, repeated = True)  # Journaleinträge
    business_items = ndb.StringProperty(repeated = True)  # Branchen
    anniversary_items = ndb.StructuredProperty(Anniversary, repeated = True)  # Jahrestage, Geburtstag
    gender = ndb.StringProperty()


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


