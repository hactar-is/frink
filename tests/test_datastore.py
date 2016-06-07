# -*- coding: utf-8 -*-

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import pytest

from app.models import User, Role
from frink.datastore import FrinkUserDatastore
from frink.errors import NotUniqueError

user_dict = {
    'firstname': 'Michael',
    'lastname': 'Harriman',
    'email': 'harriman@example.com',
    'password': 'this is a password'
}

role_dict = {
    'name': 'User',
    'description': 'A registered user.'
}


def test_user_datastore_instance(app):
    assert isinstance(app.user_datastore, FrinkUserDatastore) is True


def test_create_user(app):
    user = app.user_datastore.create_user(**user_dict)
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_create_duplicate_user(app):
    with pytest.raises(NotUniqueError):
        app.user_datastore.create_user(**user_dict)


def test_get_user(app):
    user = app.user_datastore.get_user('harriman@example.com')
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_find_user(app):
    temp_user = app.user_datastore.get_user('harriman@example.com')
    user = app.user_datastore.find_user(id=temp_user.id)
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_find_user_by_lastname(app):
    temp_user = app.user_datastore.get_user('harriman@example.com')
    user = app.user_datastore.find_user(lastname=user_dict['lastname'])
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_orm_create_role(app):
    role = Role(role_dict)
    role.validate()
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_find_role(app):
    role = app.user_datastore.find_role('User')
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_add_role_to_user(app):
    user = app.user_datastore.get_user('harriman@example.com')
    role = app.user_datastore.find_role('User')
    app.user_datastore.add_role_to_user(user, role)
    assert role in user.roles
    user.save()


def test_has_role(app):
    user = app.user_datastore.get_user('harriman@example.com')
    role = app.user_datastore.find_role('User')
    assert user.has_role(role) is True


def test_delete(app):
    user1 = app.user_datastore.get_user('harriman@example.com')
    role1 = app.user_datastore.find_role('User')
    app.user_datastore.delete(user1)
    app.user_datastore.delete(role1)
    user2 = app.user_datastore.get_user('harriman@example.com')
    role2 = app.user_datastore.find_role('User')
    assert user2 is None
    assert role2 is None
