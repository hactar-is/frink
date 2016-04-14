# -*- coding: utf-8 -*-

"""
    frink.connection
    ~~~~~~~~~~~~~
    Setup of RethinkDB stuff.
"""

from flask import abort, current_app
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

# Frink
from .registry import model_registry

import logging
log = logging.getLogger(__name__)


class rconnect(object):
    def __enter__(self):
        log.info('CONNECT ENTER')
        try:
            app = current_app
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
        log.info('CONNECT EXIT')
        self.conn.close()


class RethinkDB(object):

    def connection(self, app):
        return r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))

    def setup(self, app):
        connection = r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))
        try:
            r.db_create(app.config.get('RDB_DB')).run(connection)
            log.info('Database setup completed')
        except RqlRuntimeError:
            log.info('Database already exists.')
        finally:
            connection.close()

    def drop_all(self, app):
        conn = self.connection(app)
        return r.db_drop(app.config['RDB_DB']).run(conn)

    def disconnect(self, app=None):
        log.info('DISCONNECT')
        if app is None:
            app = self._app

        try:
            app.rdb_conn.close()
        except AttributeError:
            pass

    def connect(self, app=None):
        log.info('CONNECT')
        if app is None:
            app = self._app

        try:
            app.rdb_conn = r.connect(
                host=app.config.get('RDB_HOST'),
                port=app.config.get('RDB_PORT'),
                db=app.config.get('RDB_DB')
            )
            log.info(app.rdb_conn)
        except RqlDriverError:
            abort(503, "Database connection could be established.")

    def init_app(self, app):
        log.info('RethinkSetup.init_app')
        self._app = app
        self.setup(app)

        # open connection before each request
        @app.before_request
        def before_request():
            self.connect(app)

        # close connection at end of each request
        @app.teardown_request
        def teardown_request(exception):
            self.disconnect(app)

        # And finally...
        model_registry.init_app(app)
