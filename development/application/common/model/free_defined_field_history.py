#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


class FreeDefinedFieldHistory(ndb.Model):

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")

    free_defined_field_key = ndb.KeyProperty()
    free_defined_field_dict = ndb.PickleProperty()
