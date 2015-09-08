#!/usr/bin/env python
# coding: utf-8
"""
Startet dev_appserver.py mit den richtigen Parametern
"""

import os
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))
STORAGEDIR = os.path.join(THISDIR, "_local_datastore")

os.chdir(THISDIR)

subprocess.call(
    args = [
        os.path.expanduser(
            "~/bin/google_appengine/dev_appserver.py"
        ),
        "--host", "0.0.0.0",
        "--port", "8081",
        "--admin_port", "8001",
        "--require_indexes", "yes",
        "--storage_path", STORAGEDIR,
        "./app.yaml",
        # "./backend.yaml",
        # "./dispatch.yaml",
    ],
    cwd = THISDIR
)
