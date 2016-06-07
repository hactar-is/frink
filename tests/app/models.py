# -*- coding: utf-8 -*-

"""
    app.models
    ~~~~~~~~~~
    Data models for testing Frink.
"""

from future.utils import with_metaclass

import datetime
from schematics.types.base import (
    StringType, BooleanType, DateTimeType, IntType
)

from schematics.types.compound import (
    ListType, ModelType
)

from frink.base import BaseModel
from frink.orm import ORMMeta
from frink.types import HasOne


class Role(with_metaclass(ORMMeta, BaseModel)):

    name = StringType()
    description = StringType()


class User(with_metaclass(ORMMeta, BaseModel)):

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


class SlugTest(with_metaclass(ORMMeta, BaseModel)):

    name = StringType()
    slug = StringType()


class NameTest(with_metaclass(ORMMeta, BaseModel)):

    name = StringType()
    something = IntType()


class IdTest(with_metaclass(ORMMeta, BaseModel)):

    something = IntType()


class InvalidModel(with_metaclass(ORMMeta, BaseModel)):

    unreq = StringType()
    req = StringType(required=True)


class Child(with_metaclass(ORMMeta, BaseModel)):

    name = StringType(required=True)


class Parent(with_metaclass(ORMMeta, BaseModel)):

    name = StringType(required=True)
    child = HasOne(Child)
    spouse = HasOne("Parent")
