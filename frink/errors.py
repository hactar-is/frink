# -*- coding: utf-8 -*-

"""
    frink.errors
    ~~~~~~~~~~~~~
    Exception and Error classes
"""

import logging
from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA


def get_log(extra=None):
    m = "{}.{}".format(__name__, extra) if extra else __name__
    return logging.getLogger(m)

log = get_log()


class FrinkError(Exception):
    pass


class NotUniqueError(FrinkError):
    pass
