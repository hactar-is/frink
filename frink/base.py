# -*- coding: utf-8 -*-

"""
    frink.base
    ~~~~~~~~~~~~~
    BaseModel class
"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import datetime
from schematics.models import Model
from schematics.types.base import (
    StringType, BooleanType, DateTimeType, IntType, UUIDType
)

from .orm import ORMMeta
from .orm import InstanceLayerMixin


class BaseModel(Model, InstanceLayerMixin):

    # __metaclass__ = ORMMeta  # Do this in every model instead

    id = UUIDType()
    created_at = DateTimeType(default=datetime.datetime.now)
    updated_at = DateTimeType(default=datetime.datetime.now)

    def __repr__(self):
        if hasattr(self, 'email'):
            return u'<{}: {}>'.format(self.__class__.__name__, self.email)
        if hasattr(self, 'slug'):
            return u'<{}: {}>'.format(self.__class__.__name__, self.slug)
        if hasattr(self, 'name'):
            return u'<{}: {}>'.format(self.__class__.__name__, self.name)
        if hasattr(self, 'id'):
            return u'<{}: {}>'.format(self.__class__.__name__, self.id)
        return u'<{}: {} object>'.format(self.__class__.__name__, self.__class__.__name__)
