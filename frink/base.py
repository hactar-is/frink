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

# Frink
from .orm import InstanceLayerMixin

import logging
log = logging.getLogger(__name__)


class BaseModel(Model, InstanceLayerMixin):

    # __metaclass__ = ORMMeta  # Do this in every model instead

    id = UUIDType()
    created_at = DateTimeType(default=datetime.datetime.now)
    updated_at = DateTimeType(default=datetime.datetime.now)

    def validate(self):
        log.debug('validating')
        super(BaseModel, self).validate()

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
