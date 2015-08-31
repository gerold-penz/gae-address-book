#!/usr/bin/env python
# coding: utf-8
"""
Benutzerverwaltung
"""

import cherrypy
from google.appengine.api import users


def get_current_user():
    """
    Gibt das Benutzer-Objekt des aktuellen Benutzers zurück

    :returns: User
        .nickname
        .email

    :rtype: users.User
    """

    return users.get_current_user()


def is_current_user_admin():
    """
    Gibt `True` zurück, wenn der Benutzer ein Admin der Anwendung ist.

    Admins werden in der "frontend.ini" festgelegt.
    """

    user = get_current_user()
    return user.nickname() in cherrypy.config["security.admins"]


def get_login_url(dest_url = "/"):
    """
    Gibt die Login-URL zurück
    """

    return users.create_login_url(dest_url = dest_url)


def get_logout_url(dest_url = "/"):
    """
    Gibt die Logout-URL zurück
    """

    return users.create_logout_url(dest_url = dest_url)



