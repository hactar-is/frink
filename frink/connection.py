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


connections = []


class rconnect(object):
    def __enter__(self):
        log.debug('CONNECT ENTER')
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
            connections.append(self.conn)
            return self.conn

    def __exit__(self, type, value, traceback):
        log.debug('CONNECT EXIT')
        connections.remove(self.conn)
        self.conn.close()


class RethinkDB(object):

    def connection(self, app):
        conn = r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))
        connections.append(conn)
        return conn

    def setup(self, app):
        try:
            conn = r.connect(host=app.config.get('RDB_HOST'), port=app.config.get('RDB_PORT'))
            r.db_create(app.config.get('RDB_DB')).run(conn)
            connections.append(conn)
            connections.remove(conn)
            conn.close()
            log.debug('Database setup completed')
        except RqlRuntimeError:
            log.debug('Database already exists.')

    def drop_all(self, app):
        with rconnect() as conn:
            return r.db_drop(app.config['RDB_DB']).run(conn)

    def disconnect(self, app=None):
        log.debug('============== DISCONNECT ===============')
        if app is None:
            app = self._app

        try:
            if app.rdb_conn in connections:
                connections.remove(app.rdb_conn)
            app.rdb_conn.close()
        except AttributeError:
            pass

    def connect(self, app=None):
        log.debug('=============== CONNECT =================')
        if app is None:
            app = self._app

        try:
            app.rdb_conn = r.connect(
                host=app.config.get('RDB_HOST'),
                port=app.config.get('RDB_PORT'),
                db=app.config.get('RDB_DB')
            )
            log.info(app.rdb_conn)
            connections.append(app.rdb_conn)
            assert app.rdb_conn in connections
        except RqlDriverError:
            abort(503, "Database connection could be established.")

    def get_connection(self):
        return self._app.rdb_conn

    def init_app(self, app):
        log.debug('RethinkSetup.init_app')
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
