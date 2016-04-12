# -*- coding: utf-8 -*-

"""
    frink.tests.app.factory
    ~~~~~~~~~~~~~
    create app
"""

from flask import Flask
from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

from .core import db, security
from .settings import Config
from .models import User, Role

from frink.datastore import FrinkUserDatastore


def create_app(package_name):
    app = Flask(package_name)
    app.config.from_object(Config)
    db.init_app(app)

    user_datastore = FrinkUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)
    # security.init_app(app, user_datastore, confirm_register_form=ExtendedConfirmRegisterForm)
    app.user_datastore = user_datastore

    return app
