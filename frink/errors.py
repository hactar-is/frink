# -*- coding: utf-8 -*-

"""
    frink.errors
    ~~~~~~~~~~~~~
    Exception and Error classes
"""

import logging
log = logging.getLogger(__name__)
from schematics.exceptions import BaseError


class FrinkError(BaseError):
    def __init__(self, messages="Generic Frink error"):
        BaseError.__init__(self, messages)


class NotUniqueError(FrinkError):

    def __init__(self, messages="Something isn't unique"):
        BaseError.__init__(self, messages)
