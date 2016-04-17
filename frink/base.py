# -*- coding: utf-8 -*-

"""
    frink.base
    ~~~~~~~~~~~~~
    BaseModel class
"""

import datetime
from schematics.models import Model
from schematics.types.base import (
    StringType, BooleanType, DateTimeType, IntType, UUIDType
)

from schematics.exceptions import ValidationError

# Frink
from .orm import InstanceLayerMixin
from .errors import NotUniqueError

import logging
log = logging.getLogger(__name__)


class BaseModel(Model, InstanceLayerMixin):

    # __metaclass__ = ORMMeta  # Do this in every model instead

    _uniques = []

    id = UUIDType()
    created_at = DateTimeType(default=datetime.datetime.now)
    updated_at = DateTimeType(default=datetime.datetime.now)

    def validate(self):
        log.debug('VALIDATING')
        for field in self._uniques:
            log.debug('Validate that {} is unique'.format(field))
            if self._data.get(field, None) is None:
                raise ValidationError('Unique fields cannot be None ({})'.format(field))
            _ = self.query.get_by(column=field, value=self._data.get(field, None))
            if _ is not None and _.id != self.id:
                raise NotUniqueError('Field `{}` must be unique'.format(field))
        return super(BaseModel, self).validate()

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
