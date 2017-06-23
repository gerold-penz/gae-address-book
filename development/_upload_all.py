#!/usr/bin/env python
# coding: utf-8
"""
Hochladen des aktuellen Ordners in die GAE
"""

import os
import subprocess
import glob


THISDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTNAME = os.path.basename(THISDIR)
PROJECTVERSION = open(os.path.join(THISDIR, "_project_version.txt")).readline().strip()
NOT_INCLUDE_FILENAMES = [
    "app-skip-files.yaml",
    "app-handlers.yaml",
]

os.chdir(THISDIR)
print PROJECTNAME


def main():

    # Hochzuladende YAML-Dateien ermitteln
    yaml_files = []
    for file_path in glob.glob(os.path.join(THISDIR, "*.yaml")):
        found = False
        for not_include in NOT_INCLUDE_FILENAMES:
            if not_include in file_path:
                found = True
        if not found:
            yaml_files.append(file_path)

    # Argumente zusammensetzen
    args = [
        os.path.expanduser(
            "~/bin/google-cloud-sdk/bin/gcloud"
        ),
        "app",
        "deploy",
        "--project", PROJECTNAME,
        "--version", PROJECTVERSION,
        "--quiet",
        # "--verbosity", "info",
    ]
    args += yaml_files

    # Hochladen
    returncode = subprocess.call(args = args, cwd = THISDIR)
    if returncode != 0:
        raw_input("Press ENTER to continue...")


if __name__ == "__main__":
    main()


