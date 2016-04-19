# -*- coding: utf-8 -*-


from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import pytest
import datetime

from rethinkdb.errors import ReqlOpFailedError
from schematics.exceptions import ModelConversionError, ValidationError

from app.models import Parent, Child
from frink.registry import model_registry
from frink.datastore import FrinkUserDatastore
from frink.errors import NotUniqueError, FrinkError
from frink.types import HasOne


kid_dict = {
    'name': 'Charlie'
}


mum_dict = {
    'name': 'Alice'
}


dad_dict = {
    'name': 'Bob'
}


def test_create_child(app):
    obj = Child(kid_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == kid_dict['name']


def test_create_mum(app):
    obj = Parent(mum_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == mum_dict['name']


def test_create_dad(app):
    obj = Parent(dad_dict)
    obj.save()
    assert obj.id is not None
    assert obj.name == dad_dict['name']
