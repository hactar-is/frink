# -*- coding: utf-8 -*-

"""
    frink.connection
    ~~~~~~~~~~~~~
    Setup of RethinkDB stuff.
"""

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

# Frink
from .registry import model_registry
from . import frink

import logging
log = logging.getLogger(__name__)


connections = []


class rconnect(object):
    def __enter__(self):
        log.debug('CONNECT ENTER - {}:{}/{}'.format(frink.RDB_HOST, frink.RDB_PORT, frink.RDB_DB))
        try:
            self.conn = r.connect(
                host=frink.RDB_HOST,
                port=frink.RDB_PORT,
                db=frink.RDB_DB
            )
        except RqlDriverError as e:
            log.warn(e)
            raise
        else:
            connections.append(self.conn)
            return self.conn

    def __exit__(self, type, value, traceback):
        log.debug('CONNECT EXIT')
        connections.remove(self.conn)
        self.conn.close()


class RethinkDB(object):

    def connection(self):
        conn = r.connect(host=frink.RDB_HOST, port=frink.RDB_PORT)
        connections.append(conn)
        return conn

    def setup(self):
        conn = r.connect(host=frink.RDB_HOST, port=frink.RDB_PORT)
        if r.db_list().contains(frink.RDB_DB).run(conn) is False:
            try:
                with rconnect() as conn:
                    r.db_create(frink.RDB_DB).run(conn)
                    log.debug('Database setup completed')
            except RqlRuntimeError as e:
                log.warn(e)
                raise
        else:
            log.debug('Skipping DB creation')

    def drop_all(self):
        with rconnect() as conn:
            return r.db_drop(frink.RDB_DB).run(conn)

    def disconnect(self):
        log.debug('============== DISCONNECT ===============')

        try:
            if self.rdb_conn in connections:
                connections.remove(self.rdb_conn)
            self.rdb_conn.close()
        except AttributeError:
            pass

    def connect(self):
        log.debug('=============== CONNECT =================')

        try:
            self.rdb_conn = r.connect(
                host=frink.RDB_HOST,
                port=frink.RDB_PORT,
                db=frink.RDB_DB
            )
            connections.append(self.rdb_conn)
            assert self.rdb_conn in connections
        except RqlDriverError as e:
            log.warn(e)
            raise

    def get_connection(self):
        return self.rdb_conn

    def init(self):
        log.debug('RethinkSetup.init')
        self.setup()

        # # open connection before each request
        # @app.before_request
        # def before_request():
        #     self.connect(app)

        # # close connection at end of each request
        # @app.teardown_request
        # def teardown_request(exception):
        #     self.disconnect(app)

        # And finally...
        model_registry.init()
