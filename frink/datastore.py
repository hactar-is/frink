# -*- coding: utf-8 -*-

"""
    frink.datastore
    ~~~~~~~~~~~~~
    Flask-Security Frink datastore classes.

"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

from flask.ext.security.datastore import Datastore, UserDatastore
from flask.ext.security.utils import get_identity_attributes


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
        print(cyan('get_user({})'.format(identifier)))
        # Note: identifier here is probably an email address
        user = self.user_model.query.get(identifier)
        if user is not None:
            return user

        for attr in get_identity_attributes():
            print(cyan(attr))
            column = getattr(self.user_model, attr)
            user = self.user_model.query.get_by(column=column.name, value=identifier)
            if user is not None:
                return user
            else:
                return None

    def find_user(self, **kwargs):
        user = self.user_model.query.first(**kwargs)
        if user is not None:
            return user
        else:
            return None

    def find_role(self, role):
        return self.role_model.query.get(name=role)

    def create_user(self, **kwargs):
        print("create_user({})".format(kwargs))
        """Creates and returns a new user from the given parameters."""
        kwargs = self._prepare_create_user_args(**kwargs)
        user = self.user_model(kwargs)
        return self.put(user)
