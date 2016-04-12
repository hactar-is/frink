# -*- coding: utf-8 -*-

"""
    marv.schemas.models
    ~~~~~~~~~~~~~
    Data validation schemas for the models.
"""

import datetime
from schematics.types.base import (
    StringType, BooleanType, DateTimeType, IntType
)

from schematics.types.compound import (
    ListType, ModelType
)

from flask.ext.security import UserMixin, RoleMixin

from frink.base import BaseModel
from frink.orm import ORMMeta


class Role(BaseModel, RoleMixin):

    __metaclass__ = ORMMeta

    name = StringType()
    description = StringType()


class User(BaseModel, UserMixin):

    __metaclass__ = ORMMeta

    firstname = StringType()
    lastname = StringType()
    email = StringType()
    password = StringType()
    active = BooleanType(default=True)
    confirmed_at = DateTimeType()
    last_login_at = DateTimeType(default=datetime.datetime.now)
    current_login_at = DateTimeType(default=datetime.datetime.now)
    registered_at = DateTimeType()
    last_login_ip = StringType()
    current_login_ip = StringType()
    login_count = IntType()

    roles = ListType(ModelType(Role), default=[])


class SlugTest(BaseModel):

    __metaclass__ = ORMMeta

    name = StringType()
    slug = StringType()


class NameTest(BaseModel):

    __metaclass__ = ORMMeta

    name = StringType()
    something = IntType()


class IdTest(BaseModel):

    __metaclass__ = ORMMeta

    something = IntType()
