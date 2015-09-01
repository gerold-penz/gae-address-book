#!/usr/bin/env python
# coding: utf-8

import os
import common.constants

THISDIR = os.path.dirname(os.path.abspath(__file__))
APIDIR = os.path.abspath(os.path.join(THISDIR, ".."))
HTTPROOTDIR = os.path.join(APIDIR, "http_root")

# Ini
SECURITY_INIPATH = os.path.join(common.constants.SETTINGSDIR, "security.ini")
