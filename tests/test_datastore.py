# -*- coding: utf-8 -*-

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

from app.models import User, Role
from frink.registry import model_registry
from frink.datastore import FrinkUserDatastore

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



def test_user_datastore_instance(app, db):
    assert isinstance(app.user_datastore, FrinkUserDatastore) is True


def test_create_user(app, db):
    user = app.user_datastore.create_user(**user_dict)
    assert isinstance(user, User)
    assert user.firstname == 'Michael'
    assert user.lastname == 'Harriman'
    assert user.email == 'harriman@example.com'
    assert user.password == 'this is a password'


def test_get_user(app, db):
    user = app.user_datastore.get_user('harriman@example.com')
    assert isinstance(user, User)
    assert user.firstname == 'Michael'
    assert user.lastname == 'Harriman'
    assert user.email == 'harriman@example.com'
    assert user.password == 'this is a password'


def test_find_user(app, db):
    temp_user = app.user_datastore.get_user('harriman@example.com')
    print(magenta(type(temp_user.id)))
    user = app.user_datastore.find_user(id=temp_user.id)
    assert isinstance(user, User)
    assert user.firstname == 'Michael'
    assert user.lastname == 'Harriman'
    assert user.email == 'harriman@example.com'
    assert user.password == 'this is a password'


def test_orm_create_role(app, db):
    role = Role(role_dict)
    role.validate()
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_find_role(app, db):
    role = app.user_datastore.find_role('User')
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_add_role_to_user(app, db):
    user = app.user_datastore.get_user('harriman@example.com')
    role = app.user_datastore.find_role('User')
    app.user_datastore.add_role_to_user(user, role)
    assert role in user.roles
    user.save()


def test_has_role(app, db):
    user = app.user_datastore.get_user('harriman@example.com')
    role = app.user_datastore.find_role('User')
    assert user.has_role(role) is True


def test_delete_it_all(app, db):
    user1 = app.user_datastore.get_user('harriman@example.com')
    role1 = app.user_datastore.find_role('User')
    assert user1.delete() is True
    assert role1.delete() is True
    user2 = app.user_datastore.get_user('harriman@example.com')
    role2 = app.user_datastore.find_role('User')
    assert user2 is None
    assert role2 is None
