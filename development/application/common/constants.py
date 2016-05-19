#!/usr/bin/env python
# coding: utf-8

import os

THISDIR = os.path.dirname(os.path.abspath(__file__))
BASEDIR = os.path.abspath(os.path.join(THISDIR, "..", ".."))
SETTINGSDIR = os.path.join(BASEDIR, "settings")

# Ini
COMMON_INIPATH = os.path.join(SETTINGSDIR, "common.ini")

# Programmversion
VERSION = open(os.path.join(BASEDIR, "version.txt"), "r").readline().strip()
