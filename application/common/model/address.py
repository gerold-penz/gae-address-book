#!/usr/bin/env python
# coding: utf-8

import copy
import datetime
import common.format_
from google.appengine.ext import ndb
from google.appengine.api import search
from google.appengine.ext import deferred


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


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


# class DateTimePropertySerializable(ndb.DateTimeProperty):
#
#     def _get_for_dict(self, entity):
#
#         value = self._get_value(entity)
#
#         if value:
#             return value.isoformat()
#         else:
#             return value
#
#     def _validate(self, value):
#         if isinstance(value, basestring):
#             value = common.format_.string_to_datetime(value)
#         ndb.DateTimeProperty._validate(self, value)
#
#
#     def _db_set_value(self, v, p, value):
#         if isinstance(value, basestring):
#             value = common.format_.string_to_datetime(value)
#         ndb.DateTimeProperty._db_set_value(self, v, p, value)


class Tel(ndb.Model):
    uid = ndb.StringProperty(required = True)
    label = ndb.StringProperty()
    number = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Email(ndb.Model):
    uid = ndb.StringProperty(required = True)
    label = ndb.StringProperty()
    email = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Url(ndb.Model):
    uid = ndb.StringProperty(required = True)
    label = ndb.StringProperty()
    url = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Note(ndb.Model):
    uid = ndb.StringProperty(required = True)
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class Agreement(ndb.Model):
    uid = ndb.StringProperty(required = True)
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class JournalItem(ndb.Model):

    uid = ndb.StringProperty(required = True)
    date_time = ndb.DateTimeProperty()
    text = ndb.TextProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


    def set_date_time_iso(self, value):
        """
        Übernimmt einen ISO-Datumsstring und konvertiert diesen nach DateTime
        """

        self.date_time = common.format_.string_to_datetime(value)

    date_time_iso = property(fget = None, fset = set_date_time_iso)


class Anniversary(ndb.Model):
    uid = ndb.StringProperty(required = True)
    label = ndb.StringProperty(required = True)
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty(required = True, choices = range(1, 13))
    day = ndb.IntegerProperty(required = True)

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
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

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(
        auto_now = True, verbose_name = u"edit_timestamp"
    )
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")
    dt = ndb.DateTimeProperty(verbose_name = u"deletion_timestamp")

    # Kind
    kind = ndb.StringProperty(required = True)

    # Category Items
    category_items = ndb.StringProperty(repeated = True)

    # Tag Items
    tag_items = ndb.StringProperty(repeated = True)

    # Organization
    organization = ndb.StringProperty(indexed = False)
    organization_lower = ndb.ComputedProperty(
        lambda self: self.organization.lower() if self.organization else None
    )
    organization_char1 = ndb.ComputedProperty(
        lambda self: self.organization[0].lower() if self.organization else None
    )

    # Position
    position = ndb.StringProperty(indexed = False)
    position_lower = ndb.ComputedProperty(
        lambda self: self.position.lower() if self.position else None
    )
    position_char1 = ndb.ComputedProperty(
        lambda self: self.position[0].lower() if self.position else None
    )

    # Salutation
    salutation = ndb.StringProperty(indexed = False)
    salutation_lower = ndb.ComputedProperty(
        lambda self: self.salutation.lower() if self.salutation else None
    )
    salutation_char1 = ndb.ComputedProperty(
        lambda self: self.salutation[0].lower() if self.salutation else None
    )

    # First name
    first_name = ndb.StringProperty(indexed = False)
    first_name_lower = ndb.ComputedProperty(
        lambda self: self.first_name.lower() if self.first_name else None
    )
    first_name_char1 = ndb.ComputedProperty(
        lambda self: self.first_name[0].lower() if self.first_name else None
    )

    # Last name
    last_name = ndb.StringProperty(indexed = False)
    last_name_lower = ndb.ComputedProperty(
        lambda self: self.last_name.lower() if self.last_name else None
    )
    last_name_char1 = ndb.ComputedProperty(
        lambda self: self.last_name[0].lower() if self.last_name else None
    )

    # Nickname
    nickname = ndb.StringProperty(indexed = False)
    nickname_lower = ndb.ComputedProperty(
        lambda self: self.nickname.lower() if self.nickname else None
    )
    nickname_char1 = ndb.ComputedProperty(
        lambda self: self.nickname[0].lower() if self.nickname else None
    )

    # Street
    street = ndb.StringProperty(indexed = False)
    street_lower = ndb.ComputedProperty(
        lambda self: self.street.lower() if self.street else None
    )
    street_char1 = ndb.ComputedProperty(
        lambda self: self.street[0].lower() if self.street else None
    )

    # Postcode
    postcode = ndb.StringProperty(indexed = False)
    postcode_lower = ndb.ComputedProperty(
        lambda self: self.postcode.lower() if self.postcode else None
    )
    postcode_char1 = ndb.ComputedProperty(
        lambda self: self.postcode[0].lower() if self.postcode else None
    )

    # City
    city = ndb.StringProperty(indexed = False)
    city_lower = ndb.ComputedProperty(
        lambda self: self.city.lower() if self.city else None
    )
    city_char1 = ndb.ComputedProperty(
        lambda self: self.city[0].lower() if self.city else None
    )

    # District
    district = ndb.StringProperty(indexed = False)
    district_lower = ndb.ComputedProperty(
        lambda self: self.district.lower() if self.district else None
    )
    district_char1 = ndb.ComputedProperty(
        lambda self: self.district[0].lower() if self.district else None
    )

    # Land (Bundesland)
    land = ndb.StringProperty(indexed = False)
    land_lower = ndb.ComputedProperty(
        lambda self: self.land.lower() if self.land else None
    )
    land_char1 = ndb.ComputedProperty(
        lambda self: self.land[0].lower() if self.land else None
    )

    # Country
    country = ndb.StringProperty(indexed = False)  # Land
    country_lower = ndb.ComputedProperty(
        lambda self: self.country.lower() if self.country else None
    )
    country_char1 = ndb.ComputedProperty(
        lambda self: self.country[0].lower() if self.country else None
    )

    phone_items = ndb.StructuredProperty(Tel, repeated = True)  # Telefonnummern
    email_items = ndb.StructuredProperty(Email, repeated = True)  # E-Mail-Adressen
    url_items = ndb.StructuredProperty(Url, repeated = True)  # URLs
    journal_items = ndb.StructuredProperty(JournalItem, repeated = True)  # Journaleinträge
    business_items = ndb.StringProperty(repeated = True)  # Branchen
    anniversary_items = ndb.StructuredProperty(Anniversary, repeated = True)  # Jahrestage, Geburtstag
    gender = ndb.StringProperty()
    birthday = ndb.ComputedProperty(get_birthday_iso)
    age = property(fget = get_age)
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

        # Exclude _lower-Fields
        for property in Address._properties.values():
            if property._name.endswith("_lower"):
                exclude.append(property._name)

        # Convert address to dictionary
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
            if fieldname not in address_dict:
                continue

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
                elif key in ["category_items", "business_items", "tag_items"]:
                    if not value:
                        del address_dict[key]

        # Finished
        return address_dict


    @ndb.ComputedProperty
    def deleted(self):
        """
        Returns `True` if *DeletionTimestamp* is set.
        """

        return bool(self.dt)


    def put(self, **ctx_options):
        """
        Writes the address to the datastore.

        Adds a document to the Search-Index.
        """

        # Save address
        key = ndb.Model.put(self, **ctx_options)

        # Gather information for the index
        fields = []
        if self.kind is not None:
            fields.append(search.TextField(name = u"kind", value = self.kind))
        if self.organization is not None:
            if common.format_.has_umlauts(self.organization):
                fields.append(search.TextField(
                    name = u"organization", value = common.format_.replace_umlauts(self.organization)
                ))
            fields.append(search.TextField(name = u"organization", value = self.organization))
        if self.position is not None:
            if common.format_.has_umlauts(self.position):
                fields.append(search.TextField(
                    name = u"position", value = common.format_.replace_umlauts(self.position)
                ))
            fields.append(search.TextField(name = u"position", value = self.position))
        if self.salutation is not None:
            if common.format_.has_umlauts(self.salutation):
                fields.append(search.TextField(
                    name = u"salutation", value = common.format_.replace_umlauts(self.salutation)
                ))
            fields.append(search.TextField(name = u"salutation", value = self.salutation))
        if self.first_name is not None:
            if common.format_.has_umlauts(self.first_name):
                fields.append(search.TextField(
                    name = u"first_name", value = common.format_.replace_umlauts(self.first_name)
                ))
            fields.append(search.TextField(name = u"first_name", value = self.first_name))
        if self.last_name is not None:
            if common.format_.has_umlauts(self.last_name):
                fields.append(search.TextField(
                    name = u"last_name", value = common.format_.replace_umlauts(self.last_name)
                ))
            fields.append(search.TextField(name = u"last_name", value = self.last_name))
        if self.nickname is not None:
            if common.format_.has_umlauts(self.nickname):
                fields.append(search.TextField(
                    name = u"nickname", value = common.format_.replace_umlauts(self.nickname)
                ))
            fields.append(search.TextField(name = u"nickname", value = self.nickname))
        if self.street is not None:
            if common.format_.has_umlauts(self.street):
                fields.append(search.TextField(
                    name = u"street", value = common.format_.replace_umlauts(self.street)
                ))
            fields.append(search.TextField(name = u"street", value = self.street))
        if self.postcode is not None:
            fields.append(search.TextField(name = u"postcode", value = self.postcode))
        if self.city is not None:
            if common.format_.has_umlauts(self.city):
                fields.append(search.TextField(
                    name = u"city", value = common.format_.replace_umlauts(self.city)
                ))
            fields.append(search.TextField(name = u"city", value = self.city))
        if self.district is not None:
            if common.format_.has_umlauts(self.district):
                fields.append(search.TextField(
                    name = u"district", value = common.format_.replace_umlauts(self.district)
                ))
            fields.append(search.TextField(name = u"district", value = self.district))
        if self.land is not None:
            if common.format_.has_umlauts(self.land):
                fields.append(search.TextField(
                    name = u"land", value = common.format_.replace_umlauts(self.land)
                ))
            fields.append(search.TextField(name = u"land", value = self.land))
        if self.country is not None:
            if common.format_.has_umlauts(self.country):
                fields.append(search.TextField(
                    name = u"country", value = common.format_.replace_umlauts(self.country)
                ))
            fields.append(search.TextField(name = u"country", value = self.country))
        if self.gender is not None:
            fields.append(search.TextField(name = u"gender", value = self.gender))

        for category_item in self.category_items:
            if common.format_.has_umlauts(category_item):
                fields.append(search.TextField(
                    name = u"category", value = common.format_.replace_umlauts(category_item)
                ))
            fields.append(search.TextField(name = u"category", value = category_item))
        for tag_item in self.tag_items:
            if common.format_.has_umlauts(tag_item):
                fields.append(search.TextField(
                    name = u"tag", value = common.format_.replace_umlauts(tag_item)
                ))
            fields.append(search.TextField(name = u"tag", value = tag_item))
        for business_item in self.business_items:
            if common.format_.has_umlauts(business_item):
                fields.append(search.TextField(
                    name = u"business", value = common.format_.replace_umlauts(business_item)
                ))
            fields.append(search.TextField(name = u"business", value = business_item))
        for phone_item in self.phone_items:
            assert isinstance(phone_item, Tel)
            fields.append(search.TextField(name = u"phone", value = phone_item.number))
        for email_item in self.email_items:
            assert isinstance(email_item, Email)
            fields.append(search.TextField(name = u"email", value = email_item.email))
        for url_item in self.url_items:
            assert isinstance(url_item, Url)
            fields.append(search.TextField(name = u"url", value = url_item.url))
        for journal_item in self.journal_items:
            if common.format_.has_umlauts(journal_item):
                fields.append(search.TextField(
                    name = u"journal", value = common.format_.replace_umlauts(journal_item)
                ))
            assert isinstance(journal_item, JournalItem)
            fields.append(search.TextField(name = u"journal", value = journal_item.text))
        for note_item in self.note_items:
            if common.format_.has_umlauts(note_item.text):
                fields.append(search.TextField(
                    name = u"note", value = common.format_.replace_umlauts(note_item.text)
                ))
            assert isinstance(note_item, Note)
            fields.append(search.TextField(name = u"note", value = note_item.text))
        for agreement_item in self.agreement_items:
            if common.format_.has_umlauts(agreement_item):
                fields.append(search.TextField(
                    name = u"agreement", value = common.format_.replace_umlauts(agreement_item)
                ))
            assert isinstance(agreement_item, Agreement)
            fields.append(search.TextField(name = u"agreement", value = agreement_item.text))
        for anniversary_item in self.anniversary_items:
            assert isinstance(anniversary_item, Anniversary)
            if anniversary_item.year:
                fields.append(
                    search.DateField(
                        name = u"anniversary", value = datetime.date(
                            anniversary_item.year,
                            anniversary_item.month,
                            anniversary_item.day
                        )
                    )
                )
            else:
                fields.append(
                    search.TextField(
                        name = u"anniversary",
                        value = unicode(anniversary_item.month) + u"-" + unicode(anniversary_item.day)
                    )
                )
            fields.append(search.TextField(name = u"anniversary", value = anniversary_item.label))

        # Document
        document = search.Document(
            doc_id = key.urlsafe(),
            fields = fields
        )

        # Index (deferred)
        deferred.defer(
            _put_address_to_index,
            document = document
        )

        # Finished
        return key


def _put_address_to_index(document):
    """
    Adds the address to the search_index
    """

    index = search.Index(name = "Address")
    index.put(document)
