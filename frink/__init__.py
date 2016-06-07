# -*- coding: utf-8 -*-

"""
    Frink
    ~~~~~~~~~~~~~
    Frink is a kind of ORM thing for RethinkDB built on top of the excellent Schematics.
"""

__version__ = "0.0.7"


class Frink(object):
    RDB_HOST = '127.0.0.1'
    RDB_PORT = 28015
    RDB_DB = ''

    def init(self, db=RDB_DB, host=RDB_HOST, port=RDB_PORT):
        """Create the Frink object to store the connection credentials."""
        self.RDB_HOST = host
        self.RDB_PORT = port
        self.RDB_DB = db

        from .connection import RethinkDB
        self.rdb = RethinkDB()
        self.rdb.init()


frink = Frink()
