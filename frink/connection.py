# -*- coding: utf-8 -*-

"""
    frink.connection
    ~~~~~~~~~~~~~
    Setup of RethinkDB stuff.
"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

from flask import abort
from functools import wraps
from flask import current_app as app
from contextlib import contextmanager
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from .registry import model_registry


class rconnect(object):
    def __enter__(self):
        print(green('CONNECT ENTER'))
        try:
            self.conn = r.connect(
                host=app.config.get('RDB_HOST'),
                port=app.config.get('RDB_PORT'),
                db=app.config.get('RDB_DB')
            )
        except RqlDriverError:
            abort(503, "Database connection could be established.")
        else:
            return self.conn

    def __exit__(self, type, value, traceback):
        print(green('CONNECT EXIT'))
        self.conn.close()


class RethinkDB(object):

    def connection(self, app):
        return r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))

    def setup(self, app):
        connection = r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))
        try:
            r.db_create(app.config.get('RDB_DB')).run(connection)
            print('Database setup completed')
        except RqlRuntimeError:
            print('Database already exists.')
        finally:
            connection.close()

    def drop_all(self, app):
        conn = self.connection(app)
        return r.db_drop(app.config['RDB_DB']).run(conn)

    def init_app(self, app):

        print(magenta('RethinkSetup.init_app'))

        self.setup(app)

        # open connection before each request
        @app.before_request
        def before_request():
            print(green('CONNECT'))
            try:
                app.rdb_conn = r.connect(
                    host=app.config.get('RDB_HOST'),
                    port=app.config.get('RDB_PORT'),
                    db=app.config.get('RDB_DB')
                )
                print(green(app.rdb_conn))
            except RqlDriverError:
                abort(503, "Database connection could be established.")

        @app.teardown_request
        def teardown_request(exception):
            print(green('DISCONNECT'))
            try:
                app.rdb_conn.close()
            except AttributeError:
                pass

        # And finally...
        model_registry.init_app(app)
