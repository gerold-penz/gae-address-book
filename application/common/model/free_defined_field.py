#!/usr/bin/env python
# coding: utf-8

import copy
from google.appengine.ext import ndb


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


class FreeDefinedField(ndb.Model):

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")

    label = ndb.StringProperty(required = True)
    group = ndb.StringProperty()
    position = ndb.IntegerProperty()


    def to_dict(
        self,
        include = None,
        exclude = None,
        exclude_creation_metadata = None
    ):
        """
        Return a dict containing the entity's property values.
        """

        exclude = exclude or []
        if exclude_creation_metadata:
            exclude.extend(["ct", "cu"])

        # Convert to dictionary
        free_defined_field_dict = self._to_dict(include = include, exclude = exclude)
        free_defined_field_dict = copy.deepcopy(free_defined_field_dict)
        free_defined_field_dict["key_urlsafe"] = self.key.urlsafe()

        # Finished
        return free_defined_field_dict
