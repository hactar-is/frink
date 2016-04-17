Quickstart
==========

Flask
-----

Frink is designed to be used with the Application Factory pattern in Flask.

::
    
    from frink.connection import RethinkDB

    db = RethinkDB()


Then in your application factory, call init_app on the DB object.


::

    def create_app():
        ...
        db.init_app(app)


.. _flask-security:

Flask-Security
--------------


Frink includes ``FrinkDatastore`` and ``FrinkUserDatastore`` for Flask-Security compatibility.

Define your ``User`` and ``Role`` models.

::

    import datetime
    from schematics.types.base import (
        StringType, BooleanType, DateTimeType, IntType
    )

    from schematics.types.compound import (
        ListType, ModelType
    )

    from flask.ext.security import UserMixin, RoleMixin

    from frink.base import BaseModel
    from frink.orm import ORMMeta


    class Role(BaseModel, RoleMixin):

        __metaclass__ = ORMMeta

        name = StringType()
        description = StringType()


    class User(BaseModel, UserMixin):

        __metaclass__ = ORMMeta
        _uniques = ['email']

        email = StringType()
        password = StringType()
        active = BooleanType(default=True)
        confirmed_at = DateTimeType()
        last_login_at = DateTimeType(default=datetime.datetime.now)
        current_login_at = DateTimeType(default=datetime.datetime.now)
        registered_at = DateTimeType()
        last_login_ip = StringType()
        current_login_ip = StringType()
        login_count = IntType()

        roles = ListType(ModelType(Role))


Then in your application factory, initialise this...

::

    from frink.datastore import FrinkUserDatastore
    from .users.models import User, Role

    def create_app():
        ...
        user_datastore = FrinkUserDatastore(db, User, Role)
        security.init_app(app, user_datastore)
        app.user_datastore = user_datastore

