# -*- coding: utf-8 -*-

"""
    frink.errors
    ~~~~~~~~~~~~~
    Exception and Error classes
"""

import logging
log = logging.getLogger(__name__)


class FrinkError(Exception):
    pass


class NotUniqueError(FrinkError):
    pass
