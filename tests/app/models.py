# -*- coding: utf-8 -*-

"""
    app.models
    ~~~~~~~~~~
    Data models for testing Frink.
"""

import datetime
from schematics.types.base import (
    StringType, BooleanType, DateTimeType, IntType
)

from schematics.types.compound import (
    ListType, ModelType
)

from frink.base import BaseModel
from frink.orm import ORMMeta
# from frink.types import HasOne


class Role(BaseModel):

    __metaclass__ = ORMMeta

    name = StringType()
    description = StringType()


class User(BaseModel):

    __metaclass__ = ORMMeta

    _uniques = ['email']

    firstname = StringType()
    lastname = StringType()
    email = StringType(required=True)
    password = StringType()
    active = BooleanType(default=True)
    confirmed_at = DateTimeType()
    last_login_at = DateTimeType(default=datetime.datetime.now)
    current_login_at = DateTimeType(default=datetime.datetime.now)
    registered_at = DateTimeType()
    last_login_ip = StringType()
    current_login_ip = StringType()
    login_count = IntType()
    sort_on = IntType()

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


class InvalidModel(BaseModel):

    __metaclass__ = ORMMeta

    unreq = StringType()
    req = StringType(required=True)


class Child(BaseModel):

    __metaclass__ = ORMMeta

    name = StringType(required=True)


class Parent(BaseModel):

    __metaclass__ = ORMMeta

    name = StringType(required=True)
    # child = HasOne(Child)
    # spouse = HasOne("Parent")
