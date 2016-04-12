# -*- coding: utf-8 -*-

from app.models import User, Role
from frink.registry import model_registry
from frink.datastore import FrinkUserDatastore

user_dict = {
    'firstname': 'Michael',
    'lastname': 'Harriman',
    'email': 'harriman@example.com',
    'password': 'this is a password'
}



def test_user_datastore_instance(app, db):
    assert isinstance(app.user_datastore, FrinkUserDatastore) is True


def test_create_user(app, db):
    user = app.user_datastore.create_user(**user_dict)
    assert isinstance(user, User)
    assert user.firstname == 'Michael'
    assert user.lastname == 'Harriman'
    assert user.email == 'harriman@example.com'
    assert user.password == 'this is a password'  # Should be encrypted



# def test_get_user(app):
#     assert 'Role' in model_registry._models


# def test_find_user(app):
#     assert 'Role' in model_registry._models


# def test_find_role(app):
#     assert 'Role' in model_registry._models
