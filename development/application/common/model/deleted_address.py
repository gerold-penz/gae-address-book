#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


class DeletedAddress(ndb.Model):

    dt = ndb.DateTimeProperty(
        auto_now_add = True,
        required = True,
        verbose_name = u"deletion_timestamp"
    )
    du = ndb.StringProperty(required = True, verbose_name = u"deletion_user")

    address_dict = ndb.PickleProperty()
