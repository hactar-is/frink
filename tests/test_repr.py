# -*- coding: utf-8 -*-

import uuid
from app.models import User, SlugTest, NameTest, IdTest


email_dict = {
    'firstname': 'Michael',
    'lastname': 'Harriman',
    'email': 'harriman@example.com',
    'password': 'this is a password'
}

slug_dict = {
    'name': 'Test Name',
    'slug': 'test-name'
}

name_dict = {
    'name': 'Test Name',
    'something': 100
}

id_dict = {
    'id': uuid.uuid4(),
    'something': 100
}


def test_repr_email(base):
    obj = User(email_dict)
    assert obj.__repr__() == '<User: {}>'.format(email_dict['email'])


def test_repr_slug(base):
    obj = SlugTest(slug_dict)
    assert obj.__repr__() == '<SlugTest: {}>'.format(slug_dict['slug'])


def test_repr_name(base):
    obj = NameTest(name_dict)
    assert obj.__repr__() == '<NameTest: {}>'.format(name_dict['name'])


def test_repr_id(base):
    obj = IdTest(id_dict)
    assert obj.__repr__() == '<IdTest: {}>'.format(id_dict['id'])
