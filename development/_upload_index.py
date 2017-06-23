#!/usr/bin/env python
# coding: utf-8

import os
import subprocess


THISDIR = os.path.dirname(os.path.abspath(__file__))
PROJECTNAME = os.path.basename(THISDIR)
PROJECTVERSION = open(os.path.join(THISDIR, "_project_version.txt")).readline().strip()

os.chdir(THISDIR)
print PROJECTNAME


def main():

    # Hochzuladende YAML-Dateien ermitteln
    yaml_files = [os.path.join(THISDIR, "index.yaml")]

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
        # "--verbosity", "debug",
    ]
    args += yaml_files

    # Hochladen
    returncode = subprocess.call(args = args, cwd = THISDIR)
    if returncode != 0:
        raw_input("Press ENTER to continue...")


if __name__ == "__main__":
    main()
