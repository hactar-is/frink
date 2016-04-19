# -*- coding: utf-8 -*-

"""
    frink.registry
    ~~~~~~~~~~~~~
    Keep a record of all the models registered.
"""

import rethinkdb as r
from rethinkdb.errors import ReqlOpFailedError

import logging
log = logging.getLogger(__name__)


class ModelRegistry(object):
    def __init__(self):
        self._models = {}
        self._tables = []
        self._initialsed = False
        self._app = None

    def add(self, name, model, meta):
        log.debug('Registering {} (initialised: {})'.format(
            name, self._initialsed
        ))

        if name in self._models:
            return
        if type(model) != meta:
            raise ValueError('{} is not of type({})'.format(model, meta))
        self._models[name] = model
        if self._initialsed is True:
            # This model is appearing after init_app has already
            # run, so we need to _init_model it.
            self._init_model(name, model)

    def drop_tables(self):
        for name, model in self._models.items():
            try:
                log.info('Drop {} table'.format(model._table))
                self._conn = r.connect(
                    host=self._app.config.get('RDB_HOST'),
                    port=self._app.config.get('RDB_PORT'),
                    db=self._app.config.get('RDB_DB')
                )
                query = r.db(model._db).table_drop(model._table)
                log.info(query)
                query.run(self._conn)
                self._conn.close()
            except ReqlOpFailedError as e:
                log.debug('{} table failed to drop'.format(model._table))
            except Exception as e:
                log.warn(e)
                raise
        return True

    def init_app(self, app):
        log.debug('registry init_app')
        self._app = app
        for name, model in self._models.items():
            self._init_model(name, model)
        self._initialsed = True

    def _init_model(self, name, model):
        model._model = model
        setattr(model, '_db', self._app.config.get('RDB_DB', 'test'))
        setattr(model.query, '_db', self._app.config.get('RDB_DB', 'test'))
        self._create_table(name, model)
        self._create_relationships(name, model)

    def _create_relationships(self, name, model):
        for field in self.fields:
            from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA
            print(yellow("field {}".format(field)))

    def _create_table(self, name, model):
        if name not in self._tables:
            try:
                log.debug('create {} table for {}'.format(model._table, name))
                self._conn = r.connect(
                    host=self._app.config.get('RDB_HOST'),
                    port=self._app.config.get('RDB_PORT'),
                    db=self._app.config.get('RDB_DB')
                )
                query = r.db(model._db).table_create(model._table)
                log.info(query)
                query.run(self._conn)
                self._conn.close()
            except ReqlOpFailedError as e:
                log.debug('{} table probably already exists'.format(model._table))
            except Exception as e:
                log.warn(e)
                raise
            else:
                self._tables.append(name)


model_registry = ModelRegistry()
