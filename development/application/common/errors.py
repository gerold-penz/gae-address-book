#!/usr/bin/env python
# coding: utf-8


class GaeAddressBookError(RuntimeError):
    pass


class UserNotExistsError(GaeAddressBookError):

    def __init__(self, user):
        self.user = user


class NotAuthorizedError(GaeAddressBookError):

    def __init__(self, user, authorization):
        self.user = user
        self.authorization = authorization

