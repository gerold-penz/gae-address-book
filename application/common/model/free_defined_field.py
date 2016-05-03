#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


class FreeDefinedField(ndb.Model):

    ct = ndb.DateTimeProperty(
        auto_now_add = True, required = True, verbose_name = u"creation_timestamp"
    )
    cu = ndb.StringProperty(required = True, verbose_name = u"creation_user")

    label = ndb.StringProperty(required = True)
    position = ndb.IntegerProperty()
