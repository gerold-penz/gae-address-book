#!/usr/bin/env python
# coding: utf-8

import os
import sys
import logging

THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = os.path.abspath(os.path.join(THISDIR, "application"))
ZIPLIBSDIR = os.path.join(APPDIR, "ziplibs")

sys.path.insert(0, APPDIR)
sys.path.insert(0, os.path.join(ZIPLIBSDIR, "bunch.zip"))
sys.path.insert(0, os.path.join(ZIPLIBSDIR, "cherrypy.zip"))
sys.path.insert(0, os.path.join(ZIPLIBSDIR, "pyjsonrpc.zip"))
sys.path.insert(0, os.path.join(ZIPLIBSDIR, "docutils.zip"))
sys.path.insert(0, os.path.join(ZIPLIBSDIR, "mako.zip"))
# sys.path.insert(0, os.path.join(ZIPLIBSDIR, "cloudstorage.zip"))
# sys.path.insert(0, os.path.join(ZIPLIBSDIR, "urllib3.zip"))

logging.info("appengine_config.py - loaded")
