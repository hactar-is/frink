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
from .registry import model_registry

import logging
log = logging.getLogger(__name__)


class BaseModel(Model, InstanceLayerMixin):

    _uniques = []

    id = UUIDType()
    created_at = DateTimeType(default=datetime.datetime.now)
    updated_at = DateTimeType(default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA
        # load relationships
        super(BaseModel, self).__init__(*args, **kwargs)
        log.debug(magenta('MODEL: {}'.format(self)))
        for name, type_class in self._fields.items():
            log.debug(magenta('ATTR: {} ({})'.format(name, type_class)))
            if self.get(name, None) is not None:
                log.debug(magenta('ATTR 2: {} ({})'.format(name, type_class)))
                if type_class.__class__.__name__ == 'HasOne':
                    sub_model = model_registry.find(type_class.model_class)
                    sub = sub_model.query.get(self.get(name))
                    setattr(self, name, sub)
                    assert isinstance(self.get(name), sub_model)


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
