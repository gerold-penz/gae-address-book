#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb


# ACHTUNG! Neue Models müssen auch in den Backup-Cron-Job eingetragen werden!


class NamedValue(ndb.Model):
    name = ndb.StringProperty()
    value = ndb.PickleProperty()

