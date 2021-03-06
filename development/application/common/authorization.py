#!/usr/bin/env python
# coding: utf-8

import cherrypy
import errors

# Authorizations
ADDRESS_CREATE = "address.create"

OWN_ADDRESS_READ = "own_address.read"
OWN_ADDRESS_EDIT = "own_address.edit"
OWN_ADDRESS_DELETE = "own_address.delete"

PUBLIC_ADDRESS_READ = "public_address.read"
PUBLIC_ADDRESS_EDIT = "public_address.edit"
PUBLIC_ADDRESS_DELETE = "public_address.delete"

PRIVATE_ADDRESS_READ = "private_address.read"
PRIVATE_ADDRESS_EDIT = "private_address.edit"
PRIVATE_ADDRESS_DELETE = "private_address.delete"

FREE_DEFINED_FIELD_CREATE = "free_defined_field.create"
FREE_DEFINED_FIELD_EDIT = "free_defined_field.edit"

# All authorizations
ALL_AUTHORIZATIONS = {
    ADDRESS_CREATE,

    OWN_ADDRESS_READ,
    OWN_ADDRESS_EDIT,
    OWN_ADDRESS_DELETE,

    PUBLIC_ADDRESS_READ,
    PUBLIC_ADDRESS_EDIT,
    PUBLIC_ADDRESS_DELETE,

    PRIVATE_ADDRESS_READ,
    PRIVATE_ADDRESS_EDIT,
    PRIVATE_ADDRESS_DELETE,

    FREE_DEFINED_FIELD_CREATE,
    FREE_DEFINED_FIELD_EDIT
}

# Default authorizations for roles
DEFAULT_AUTHORIZATIONS = {
    "address.create": ["user", "main_user", "admin"],

    "own_address.read": ["viewer", "user", "main_user", "admin"],
    "own_address.edit": ["user", "main_user", "admin"],
    "own_address.delete": ["user", "main_user", "admin"],

    "public_address.read": ["viewer", "user", "main_user", "admin"],
    "public_address.edit": ["user", "main_user", "admin"],
    "public_address.delete": ["main_user", "admin"],

    "private_address.read": ["main_user", "admin"],
    "private_address.edit": ["admin"],
    "private_address.delete": ["admin"],

    "free_defined_field.create": ["admin"],
    "free_defined_field.edit": ["admin"],
}


# Global authorizations
_authorizations = None


def get_authorizations():
    """
    Returns a combination between default authorizations and INI-settings
    """

    global _authorizations

    if _authorizations:
        return _authorizations

    _authorizations = DEFAULT_AUTHORIZATIONS.copy()
    _authorizations.update(cherrypy.config["authorizations"])

    # Finished
    return _authorizations


def check_authorization(user, authorization):
    """
    Checks if the user has the authorization.

    Raises an error if not.
    """

    assert authorization in ALL_AUTHORIZATIONS

    # Check if user exists
    if user not in cherrypy.config["users"]:
        raise errors.UserNotExistsError(user = user)

    # Get authorizations
    authorizations = get_authorizations()

    # Get roles for authorization
    role_names = authorizations.get(authorization)
    if not role_names:
        raise errors.NotAuthorizedError(user = user, authorization = authorization)

    # Check usernames in roles
    for role_name in role_names:
        if user in cherrypy.config["roles"][role_name]:
            break
    else:
        raise errors.NotAuthorizedError(user = user, authorization = authorization)


