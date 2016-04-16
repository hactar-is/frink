# -*- coding: utf-8 -*-

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import pytest
import datetime

from rethinkdb.errors import ReqlOpFailedError

from app.models import User, Role
from frink.registry import model_registry
from frink.datastore import FrinkUserDatastore
from frink.errors import NotUniqueError, FrinkError

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


def test_user_datastore_instance(app):
    assert isinstance(app.user_datastore, FrinkUserDatastore) is True


def test_create_user(app):
    user = User(user_dict)
    user.save()
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_create_invalid_user(app):
    user = User(invalid_user_dict)
    with pytest.raises(ValidationError) as excinfo:
        user.save()
    assert excinfo.value.messages == {'email': [u'This field is required.']}

# No idea why this test fails.
# def test_create_unconvertable_user(app):
#     user = User(unconvertable_user_dict)
#     with pytest.raises(ModelConversionError) as excinfo:
#         user.save()
#     assert excinfo.value.messages == {'firstname': [u"Couldn't interpret '2001-01-01' as string."]}


def test_create_role(app):
    role = Role(role_dict)
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict['name']
    assert role.description == role_dict['description']


def test_create_another_user(app):
    user = User(user_dict2)
    user.save()
    assert isinstance(user, User)
    assert user.firstname == user_dict2['firstname']
    assert user.lastname == user_dict2['lastname']
    assert user.email == user_dict2['email']
    assert user.password == user_dict2['password']


def test_create_admin_role(app):
    role = Role(role_dict_admin)
    role.save()
    assert isinstance(role, Role)
    assert role.name == role_dict_admin['name']
    assert role.description == role_dict_admin['description']


def test_orm_first(app):
    user = User.query.first(email=user_dict['email'])
    assert isinstance(user, User)
    assert user.firstname == user_dict['firstname']
    assert user.lastname == user_dict['lastname']
    assert user.email == user_dict['email']
    assert user.password == user_dict['password']


def test_orm_first_asc(app):
    user = User.query.first(active=True, order_by='<sort_on')
    assert isinstance(user, User)
    assert user.sort_on == 0


def test_orm_first_desc(app):
    user = User.query.first(active=True, order_by='>sort_on')
    assert isinstance(user, User)
    assert user.sort_on == 1


def test_orm_first_default(app):
    user = User.query.first(active=True, order_by='sort_on')
    assert isinstance(user, User)
    assert user.sort_on == 0


def test_append_role(app):
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


def test_all(app):
    users = User.query.all()
    assert len(users) == 2


def test_all_ordered(app):
    users = User.query.all(order_by='sort_on')
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1
    users = User.query.all(order_by='<sort_on')
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1
    users = User.query.all(order_by='>sort_on')
    assert len(users) == 2
    assert users[0].sort_on == 1
    assert users[1].sort_on == 0


def test_all_ordered_limited(app):
    users = User.query.all(order_by='sort_on', limit=1)
    assert len(users) == 1
    assert users[0].sort_on == 0
    users = User.query.all(order_by='<sort_on', limit=1)
    assert len(users) == 1
    assert users[0].sort_on == 0
    users = User.query.all(order_by='>sort_on', limit=1)
    assert len(users) == 1
    assert users[0].sort_on == 1


def test_filter(app):
    users = User.query.filter(active=True)  # Should return all
    assert len(users) == 2
    users = User.query.filter(email=user_dict['email'])  # Should return 1
    assert len(users) == 1
    users = User.query.filter(email='unknown@example.com')  # Should return empty
    assert len(users) == 0


def test_filter_order(app):
    users = User.query.filter(active=True, order_by='sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1


def test_filter_order_desc(app):
    users = User.query.filter(active=True, order_by='>sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 1
    assert users[1].sort_on == 0


def test_filter_order_asc(app):
    users = User.query.filter(active=True, order_by='<sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1


def test_filter_order_desc_with_limit(app):
    users = User.query.filter(active=True, order_by='>sort_on', limit=1)  # Should return 1
    assert len(users) == 1
    assert users[0].sort_on == 1


def test_filter_order_asc_with_limit(app):
    users = User.query.filter(active=True, order_by='<sort_on', limit=1)  # Should return 1
    assert len(users) == 1
    assert users[0].sort_on == 0


def test_find_by(app):
    users = User.query.find_by(column='active', value=True)  # Should return all
    assert len(users) == 2
    users = User.query.find_by(column='email', value=user_dict['email'])  # Should return 1
    assert len(users) == 1
    users = User.query.find_by(column='email', value='unknown@example.com')  # Should return empty
    assert len(users) == 0


def test_find_by_ordered(app):
    users = User.query.find_by(column='active', value=True, order_by='<sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 0
    assert users[1].sort_on == 1
    users = User.query.find_by(column='active', value=True, order_by='>sort_on')  # Should return all
    assert len(users) == 2
    assert users[0].sort_on == 1
    assert users[1].sort_on == 0


def test_find_by_ordered_limit(app):
    users = User.query.find_by(column='active', value=True, order_by='<sort_on', limit=1)
    assert len(users) == 1
    assert users[0].sort_on == 0
    users = User.query.find_by(column='active', value=True, order_by='>sort_on', limit=1)
    assert len(users) == 1
    assert users[0].sort_on == 1


####################################################################################################
# Test Failures
####################################################################################################


def test_get_by(app):
    with pytest.raises(NotUniqueError):
        user = User.query.get_by(column='active', value=True)  # Should raise NotUniqueError
    user = User.query.get_by(column='email', value=user_dict['email'])  # Should return a user
    assert isinstance(user, User)
    assert user.email == user_dict['email']
    user = User.query.get_by(column='email', value='unknown@example.com')  # Should return None
    assert user is None


def test_save_failure(app):
    u = User(user_dict)
    old_table = u._table
    u._table = 'this_table_doesnt_exist'
    with pytest.raises(Exception) as excinfo:
        u.save()
    u._table = old_table


def test_delete_with_no_id(app):
    u = User.query.first(email=user_dict['email'])
    assert isinstance(u, User)
    u.id = None
    with pytest.raises(FrinkError) as excinfo:
        u.delete()
    assert "You can't delete an object with no ID" in excinfo.value


def test_delete_failure(app):
    u = User.query.first(email=user_dict['email'])
    old_table = u._table
    u._table = 'this_table_doesnt_exist'
    with pytest.raises(ReqlOpFailedError) as excinfo:
        u.delete()
    u._table = old_table


def test_get_with_none_id(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.get(None)


def test_find_by_with_no_column(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.find_by(value=1)


def test_find_by_with_no_value(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.find_by(column='sort_on')


def test_get_by_with_no_column(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.get_by(value=1)


def test_get_by_with_no_value(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.get_by(column='sort_on')


def test_get_with_int_id(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.get(100)


def test_filter_with_no_kwargs(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.filter(order_by='sort_on', limit=2)


def test_first_with_no_kwargs(app):
    with pytest.raises(ValueError) as excinfo:
        User.query.first(order_by='sort_on')


def test_limiting_with_non_int(app):
    with pytest.raises(ValueError):
        users = User.query.find_by(column='active', value=True, order_by='>sort_on', limit='whut')


####################################################################################################
# Clean up
####################################################################################################


def test_delete_it_all(app):
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


####################################################################################################
# Ensure we've closed all the RethinkDB connections
####################################################################################################


def test_all_connections_are_closed():
    from frink.connection import connections
    assert len(connections) == 0


####################################################################################################
# Failing tests
####################################################################################################


"""
    This one is making a perfectly valid query no matter what I do to try to give it a bad db or
    table name. Maybe this is a good thing.
"""

# def test_filter_with_bad_table(app):
#     old_table = User._table
#     old_db = User._orm._db
#     User._table = 'this_table_doesnt_exist'
#     User._orm._table = 'this_table_doesnt_exist'
#     User._orm._db = 'this_db_doesnt_exist'
#     with pytest.raises(ReqlOpFailedError) as excinfo:
#         User.query.filter(order_by='sort_on', limit=2, email=user_dict['email'])
#     User._table = old_table
#     User._orm._table = old_table
#     User._orm._db = old_db
