#!/usr/bin/env python
# coding: utf-8

import copy
import datetime
import cherrypy
import common.format_
from google.appengine.ext import ndb
from google.appengine.api import search
# from google.appengine.ext import deferred


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


class ItemsBase(ndb.Model):

    uid = ndb.StringProperty(required = True)

    ct = ndb.DateTimeProperty(required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")


class TelItem(ItemsBase):
    label = ndb.StringProperty()
    number = ndb.StringProperty(required = True)


class EmailItem(ItemsBase):
    label = ndb.StringProperty()
    email = ndb.StringProperty(required = True)


class UrlItem(ItemsBase):
    label = ndb.StringProperty()
    url = ndb.StringProperty(required = True)


class NoteItem(ItemsBase):
    text = ndb.TextProperty(required = True)


class JournalItem(NoteItem):
    pass


class AgreementItem(NoteItem):
    pass


class AnniversaryItem(ItemsBase):
    label = ndb.StringProperty(required = True)
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty(choices = range(1, 13))
    day = ndb.IntegerProperty(choices = range(1, 32))


class FreeDefinedItem(ItemsBase):
    group = ndb.StringProperty(required = True)
    label = ndb.StringProperty(required = True)
    text = ndb.TextProperty(required = True)


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
            assert isinstance(anniversary_item, AnniversaryItem)
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
            assert isinstance(anniversary_item, AnniversaryItem)
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

    ct = ndb.DateTimeProperty(required = True, verbose_name = u"creation_timestamp")
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")
    et = ndb.DateTimeProperty(required = True, verbose_name = u"edit_timestamp")
    eu = ndb.StringProperty(required = True, verbose_name = u"edit_user")

    kind = ndb.StringProperty(required = True)
    category_items = ndb.StringProperty(repeated = True)
    organization = ndb.StringProperty()
    position = ndb.StringProperty()
    salutation = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    nickname = ndb.StringProperty()
    street = ndb.StringProperty()
    postcode = ndb.StringProperty()
    city = ndb.StringProperty()
    district = ndb.StringProperty()
    land = ndb.StringProperty()
    country = ndb.StringProperty()  # Land
    gender = ndb.StringProperty()
    birthday = ndb.ComputedProperty(get_birthday_iso)
    age = property(fget = get_age)

    tag_items = ndb.StringProperty(repeated = True)
    business_items = ndb.StringProperty(repeated = True)  # Branchen

    phone_items = ndb.LocalStructuredProperty(TelItem, repeated = True)  # Telefonnummern
    email_items = ndb.LocalStructuredProperty(EmailItem, repeated = True)  # E-Mail-Adressen
    url_items = ndb.LocalStructuredProperty(UrlItem, repeated = True)  # URLs

    note_items = ndb.LocalStructuredProperty(NoteItem, repeated = True, compressed = True)  # Notizen
    journal_items = ndb.LocalStructuredProperty(JournalItem, repeated = True, compressed = True)  # Journaleinträge
    agreement_items = ndb.LocalStructuredProperty(AgreementItem, repeated = True, compressed = True)  # Vereinbarungen
    free_defined_items = ndb.LocalStructuredProperty(FreeDefinedItem, repeated = True, compressed = True)  # Frei definierbare Felder
    anniversary_items = ndb.LocalStructuredProperty(AnniversaryItem, repeated = True, compressed = True)  # Jahrestage, Geburtstag


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
            "agreement_items",
            "free_defined_items",
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


    def put(self, **ctx_options):
        """
        Writes the address to the datastore.

        Adds a document to the Search-Index.
        """

        # Save address
        key = ndb.Model.put(self, **ctx_options)

        # Update search index
        self.update_search_index()

        # Finished
        return key


    def update_search_index(self):
        """
        Updates the address search index with the values of this address.
        """

        # Gather information for the index
        fields = []

        # fields.append(search.AtomField(name = u"all", value = "1"))

        if self.kind is not None:
            fields.append(search.AtomField(name = u"kind", value = self.kind))

        if self.organization is not None:
            fields.append(search.TextField(name = u"organization", value = self.organization))
            if self.organization:
                if common.format_.has_umlauts(self.organization):
                    fields.append(search.TextField(
                        name = u"organization",
                        value = common.format_.replace_umlauts(self.organization)
                    ))
                fields.append(
                    search.AtomField(name = u"organization_char1", value = self.organization[0].lower())
                )

        if self.position is not None:
            fields.append(search.TextField(name = u"position", value = self.position))
            if self.position:
                if common.format_.has_umlauts(self.position):
                    fields.append(search.TextField(
                        name = u"position",
                        value = common.format_.replace_umlauts(self.position)
                    ))
                fields.append(
                    search.AtomField(name = u"position_char1", value = self.position[0].lower())
                )

        if self.salutation is not None:
            fields.append(search.TextField(name = u"salutation", value = self.salutation))
            if self.salutation:
                if common.format_.has_umlauts(self.salutation):
                    fields.append(search.TextField(
                        name = u"salutation",
                        value = common.format_.replace_umlauts(self.salutation)
                    ))
                fields.append(
                    search.AtomField(name = u"salutation_char1", value = self.salutation[0].lower())
                )

        if self.first_name is not None:
            fields.append(search.TextField(name = u"first_name", value = self.first_name))
            if self.first_name:
                if common.format_.has_umlauts(self.first_name):
                    fields.append(search.TextField(
                        name = u"first_name",
                        value = common.format_.replace_umlauts(self.first_name)
                    ))
                fields.append(
                    search.AtomField(name = u"first_name_char1", value = self.first_name[0].lower())
                )

        if self.last_name is not None:
            fields.append(search.TextField(name = u"last_name", value = self.last_name))
            if self.last_name:
                if common.format_.has_umlauts(self.last_name):
                    fields.append(search.TextField(
                        name = u"last_name",
                        value = common.format_.replace_umlauts(self.last_name)
                    ))
                fields.append(
                    search.AtomField(name = u"last_name_char1", value = self.last_name[0].lower())
                )

        if self.nickname is not None:
            fields.append(search.TextField(name = u"nickname", value = self.nickname))
            if self.nickname:
                if common.format_.has_umlauts(self.nickname):
                    fields.append(search.TextField(
                        name = u"nickname",
                        value = common.format_.replace_umlauts(self.nickname)
                    ))
                fields.append(
                    search.AtomField(name = u"nickname_char1", value = self.nickname[0].lower())
                )

        if self.street is not None:
            fields.append(search.TextField(name = u"street", value = self.street))
            if self.street:
                if common.format_.has_umlauts(self.street):
                    fields.append(search.TextField(
                        name = u"street", value = common.format_.replace_umlauts(self.street)
                    ))
                fields.append(
                    search.AtomField(name = u"street_char1", value = self.street[0].lower())
                )

        if self.postcode is not None:
            fields.append(search.TextField(name = u"postcode", value = self.postcode))
            if self.postcode:
                fields.append(
                    search.AtomField(name = u"postcode_char1", value = self.postcode[0].lower())
                )

        if self.city is not None:
            fields.append(search.TextField(name = u"city", value = self.city))
            if self.city:
                if common.format_.has_umlauts(self.city):
                    fields.append(search.TextField(
                        name = u"city",
                        value = common.format_.replace_umlauts(self.city)
                    ))
                fields.append(
                    search.AtomField(name = u"city_char1", value = self.city[0].lower())
                )

        if self.district is not None:
            fields.append(search.TextField(name = u"district", value = self.district))
            if self.district:
                if common.format_.has_umlauts(self.district):
                    fields.append(search.TextField(
                        name = u"district",
                        value = common.format_.replace_umlauts(self.district)
                    ))

        if self.land is not None:
            fields.append(search.TextField(name = u"land", value = self.land))
            if self.land:
                if common.format_.has_umlauts(self.land):
                    fields.append(search.TextField(
                        name = u"land",
                        value = common.format_.replace_umlauts(self.land)
                    ))

        if self.country is not None:
            fields.append(search.TextField(name = u"country", value = self.country))
            if self.country:
                if common.format_.has_umlauts(self.country):
                    fields.append(search.TextField(
                        name = u"country",
                        value = common.format_.replace_umlauts(self.country)
                    ))

        if self.gender is not None:
            fields.append(search.TextField(name = u"gender", value = self.gender))

        for category_item in self.category_items:
            fields.append(search.TextField(name = u"category", value = category_item))
            if category_item:
                if common.format_.has_umlauts(category_item):
                    fields.append(search.TextField(
                        name = u"category",
                        value = common.format_.replace_umlauts(category_item)
                    ))

        for tag_item in self.tag_items:
            fields.append(search.TextField(name = u"tag", value = tag_item))
            if tag_item:
                if common.format_.has_umlauts(tag_item):
                    fields.append(search.TextField(
                        name = u"tag",
                        value = common.format_.replace_umlauts(tag_item)
                    ))

        for business_item in self.business_items:
            fields.append(search.TextField(name = u"business", value = business_item))
            if business_item:
                if common.format_.has_umlauts(business_item):
                    fields.append(search.TextField(
                        name = u"business",
                        value = common.format_.replace_umlauts(business_item)
                    ))

        for phone_item in self.phone_items:
            if phone_item.number is not None:
                fields.append(search.TextField(name = u"phone", value = phone_item.number))

        for email_item in self.email_items:
            if email_item.email is not None:
                fields.append(search.TextField(name = u"email", value = email_item.email))

        for url_item in self.url_items:
            if url_item.url is not None:
                fields.append(search.TextField(name = u"url", value = url_item.url))

        for free_defined_item in self.free_defined_items:

            name = common.format_.safe_ascii(
                free_defined_item.label.lower().replace(" ", "_").replace("-", "_")
            )
            # This fields will not indexed
            if name in cherrypy.config["search_index.address.free_defined_fields.exceptions"]:
                continue

            value = free_defined_item.text

            if value is not None:
                fields.append(search.TextField(name = name, value = value))

                if value:
                    if common.format_.has_umlauts(free_defined_item.text):
                        fields.append(search.TextField(
                            name = name,
                            value = common.format_.replace_umlauts(value)
                        ))

        for anniversary_item in self.anniversary_items:

            name = common.format_.safe_ascii(
                anniversary_item.label.lower().replace(" ", "_").replace("-", "_")
            )
            value = u""

            if anniversary_item.year and anniversary_item.month and anniversary_item.day:
                value = datetime.date(
                    int(anniversary_item.year),
                    int(anniversary_item.month),
                    int(anniversary_item.day)
                )
                fields.append(search.DateField(name = name, value = value))
            else:
                if anniversary_item.year:
                    value += unicode(anniversary_item.year) + "-"
                if anniversary_item.month:
                    value += unicode(anniversary_item.month).rjust(2, "0") + "-"
                if anniversary_item.day:
                    value += unicode(anniversary_item.day).rjust(2, "0")
                value = value.rstrip("-")

                fields.append(search.TextField(name = name, value = value))

        # for note_item in self.note_items:
        #     if common.format_.has_umlauts(note_item.text):
        #         fields.append(search.TextField(
        #             name = u"note", value = common.format_.replace_umlauts(note_item.text)
        #         ))
        #     assert isinstance(note_item, NoteItem)
        #     fields.append(search.TextField(name = u"note", value = note_item.text))

        # for journal_item in self.journal_items:
        #     if common.format_.has_umlauts(journal_item.text):
        #         fields.append(search.TextField(
        #             name = u"journal", value = common.format_.replace_umlauts(journal_item.text)
        #         ))
        #     assert isinstance(journal_item, JournalItem)
        #     fields.append(search.TextField(name = u"journal", value = journal_item.text))

        # for agreement_item in self.agreement_items:
        #     if common.format_.has_umlauts(agreement_item.text):
        #         fields.append(search.TextField(
        #             name = u"agreement", value = common.format_.replace_umlauts(agreement_item.text)
        #         ))
        #     assert isinstance(agreement_item, AgreementItem)
        #     fields.append(search.TextField(name = u"agreement", value = agreement_item.text))

        # Document
        document = search.Document(
            doc_id = self.key.urlsafe(),
            fields = fields,
            language = cherrypy.config["LANGUAGE"]
        )

        # Add/update index
        index = search.Index(name = "Address")
        index.put(document)

        # # Index (deferred)
        # deferred.defer(
        #     _put_address_to_index,
        #     document = document
        # )





        # ToDo: Notizen, Journal und Vereinbarungen in einen eigenen Index ablegen





# def _put_address_to_index(document):
#     """
#     Adds the address to the search_index
#     """
#
#     index = search.Index(name = "Address")
#     index.put(document)


