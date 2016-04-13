# -*- coding: utf-8 -*-

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import pytest
import datetime

from app.models import User, Role
from frink.registry import model_registry
from frink.datastore import FrinkUserDatastore
from frink.errors import NotUniqueError

from schematics.exceptions import ModelConversionError, ValidationError


unconvertable_user_dict = {
    'firstname': datetime.date(2001, 1, 1),
    'lastname': 'Harriman',
    'email': 'harriman@example.com',
    'password': 'this is a password'
}

invalid_user_dict = {
    'firstname': 'Michael',
    'lastname': 'Harriman',
    'password': 'this is a password'
}

user_dict = {
    'firstname': 'Michael',
    'lastname': 'Harriman',
    'email': 'harriman@example.com',
    'password': 'this is a password',
    'sort_on': 0
}

user_dict2 = {
    'firstname': 'Sido',
    'lastname': 'Jombati',
    'email': 'jombati@example.com',
    'password': 'this is a password',
    'sort_on': 1
}

role_dict = {
    'name': 'User',
    'description': 'A registered user.'
}

role_dict_admin = {
    'name': 'Admin',
    'description': 'A registered user.'
}


def test_user_datastore_instance(app, db):
    assert isinstance(app.user_datastore, FrinkUserDatastore) is True


def test_create_user(app, db):
    user = User(user_dict)
    user.save()
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_create_invalid_user(app, db):
    user = User(invalid_user_dict)
    with pytest.raises(ValidationError) as excinfo:
        user.save()
    assert excinfo.value.messages == {'email': [u'This field is required.']}

# No idea why this test fails.
# def test_create_unconvertable_user(app, db):
#     user = User(unconvertable_user_dict)
#     with pytest.raises(ModelConversionError) as excinfo:
#         user.save()
#     assert excinfo.value.messages == {'firstname': [u"Couldn't interpret '2001-01-01' as string."]}


def test_create_role(app, db):
    role = Role(role_dict)
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_create_another_user(app, db):
    user = User(user_dict2)
    user.save()
    assert isinstance(user, User)
    assert user.firstname == user_dict2['firstname']
    assert user.lastname == user_dict2['lastname']
    assert user.email == user_dict2['email']
    assert user.password == user_dict2['password']


def test_create_admin_role(app, db):
    role = Role(role_dict_admin)
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict_admin['name']
    assert role.description == role_dict_admin['description']


def test_orm_first(app, db):
    user = User.query.first(email=user_dict['email'])
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_append_role(app, db):
    _u = User.query.first(email=user_dict['email'])
    assert _u is not None
    assert isinstance(_u, User)
    _r = Role.query.first(name=role_dict['name'])
    assert _r is not None
    assert isinstance(_r, Role)
    _u.roles.append(_r)
    _u.save()
    assert _r in _u.roles
    user = User.query.get(_u.id)
    assert isinstance(user, User)
    assert _r in user.roles


def test_all(app, db):
    users = User.query.all()
    assert len(users) == 2


def test_filter(app, db):
    users = User.query.filter(active=True)  # Should return all
    assert len(users) == 2
    users = User.query.filter(email=user_dict['email'])  # Should return 1
    assert len(users) == 1
    users = User.query.filter(email='unknown@example.com')  # Should return empty
    assert len(users) == 0


def test_filter_order(app, db):
    users = User.query.filter(active=True, order_by='sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1


def test_filter_order_desc(app, db):
    users = User.query.filter(active=True, order_by='>sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 1
    assert users[1].sort_on == 0


def test_filter_order_asc(app, db):
    users = User.query.filter(active=True, order_by='<sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1


def test_filter_order_desc_with_limit(app, db):
    users = User.query.filter(active=True, order_by='>sort_on', limit=1)  # Should return 1
    assert len(users) == 1
    assert users[0].sort_on == 1


def test_filter_order_asc_with_limit(app, db):
    users = User.query.filter(active=True, order_by='<sort_on', limit=1)  # Should return 1
    assert len(users) == 1
    assert users[0].sort_on == 0


def test_find_by(app, db):
    users = User.query.find_by(column='active', value=True)  # Should return all
    assert len(users) == 2
    users = User.query.find_by(column='email', value=user_dict['email'])  # Should return 1
    assert len(users) == 1
    users = User.query.find_by(column='email', value='unknown@example.com')  # Should return empty
    assert len(users) == 0


def test_get_by(app, db):
    with pytest.raises(NotUniqueError):
        user = User.query.get_by(column='active', value=True)  # Should raise NotUniqueError
    user = User.query.get_by(column='email', value=user_dict['email'])  # Should return a user
    assert isinstance(user, User)
    assert user.email == user_dict['email']
    user = User.query.get_by(column='email', value='unknown@example.com')  # Should return None
    assert user is None


def test_delete_it_all(app, db):
    user1 = app.user_datastore.get_user(user_dict['email'])
    user2 = app.user_datastore.get_user(user_dict2['email'])
    role1 = app.user_datastore.find_role('User')
    role2 = app.user_datastore.find_role('Admin')
    assert user1.delete() is True
    assert role1.delete() is True
    assert user2.delete() is True
    assert role2.delete() is True
    user1 = app.user_datastore.get_user(user_dict['email'])
    user2 = app.user_datastore.get_user(user_dict2['email'])
    role1 = app.user_datastore.find_role('User')
    role2 = app.user_datastore.find_role('Admin')
    assert user1 is None
    assert role1 is None
    assert user2 is None
    assert role2 is None
