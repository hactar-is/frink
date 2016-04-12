# -*- coding: utf-8 -*-

"""
    frink.datastore
    ~~~~~~~~~~~~~
    Flask-Security Frink datastore classes.

"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

from flask.ext.security.datastore import Datastore, UserDatastore
from flask.ext.security.utils import get_identity_attributes

from .errors import NotUniqueError


class FrinkDatastore(Datastore):
    def put(self, model):
        model.save()
        return model

    def delete(self, model):
        model.delete()


class FrinkUserDatastore(FrinkDatastore, UserDatastore):
    """A RethinkDB / Schematics datastore implementation for Flask-Security
    """
    def __init__(self, db, user_model, role_model):
        FrinkDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def get_user(self, identifier):
        # Note: identifier here is probably an email address
        user = self.user_model.query.get(identifier)
        if user is not None:
            return user

        for attr in get_identity_attributes():
            column = getattr(self.user_model, attr)
            user = self.user_model.query.get_by(column=column.name, value=identifier)
            if user is not None:
                return user
            else:
                return None

    def find_user(self, **kwargs):
        print(cyan('find_user({})'.format(kwargs)))
        if kwargs.get('id', None) is not None:
            user = self.user_model.query.get(kwargs['id'])
            if user is not None:
                return user
        # If it's looking up by something else...
        user = self.user_model.query.first(**kwargs)
        if user is not None:
            return user

        return None

    def find_role(self, role):
        return self.role_model.query.first(name=role)

    def create_user(self, **kwargs):
        """Creates and returns a new user from the given parameters."""
        kwargs = self._prepare_create_user_args(**kwargs)
        user = self.user_model(kwargs)
        if self.get_user(user.email) is not None:
            raise NotUniqueError
        try:
            user.validate()
        except:
            raise
        else:
            user = self.put(user)
            return user
        return False
