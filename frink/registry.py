# -*- coding: utf-8 -*-

"""
    frink.registry
    ~~~~~~~~~~~~~
    Keep a record of all the models registered.
"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA
import rethinkdb as r
from rethinkdb.errors import ReqlOpFailedError


class ModelRegistry(object):
    def __init__(self):
        self._models = {}
        self._tables = []
        self._initialsed = False
        self._app = None

    def add(self, name, model, meta):
        print(green('Registering {} (initialised: {})'.format(
            name, self._initialsed
        )))

        if name in self._models:
            return
        if type(model) != meta:
            raise ValueError('{} is not of type({})'.format(model, meta))
        self._models[name] = model
        if self._initialsed is True:
            # This model is appearing after init_app has already
            # run, so we need to _init_model it.
            self._init_model(name, model)

    def init_app(self, app):
        print(green('registry init_app'))
        self._app = app
        for name, model in self._models.items():
            self._init_model(name, model)
        self._initialsed = True

    def _init_model(self, name, model):
        model._model = model
        setattr(model, '_db', self._app.config.get('RDB_DB', 'test'))
        setattr(model.query, '_db', self._app.config.get('RDB_DB', 'test'))
        if name not in self._tables:
            try:
                print(green('create {} table for {}'.format(model._table, name)))
                self._conn = r.connect(
                    host=self._app.config.get('RDB_HOST'),
                    port=self._app.config.get('RDB_PORT'),
                    db=self._app.config.get('RDB_DB')
                )
                r.db(model._db).table_create(model._table).run(self._conn)
                self._conn.close()
            except ReqlOpFailedError as e:
                print(yellow('{} table probably already exists'.format(model._table)))
            except Exception as e:
                print(red(e))
                raise
            else:
                self._tables.append(name)


model_registry = ModelRegistry()
