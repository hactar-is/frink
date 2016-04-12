# -*- coding: utf-8 -*-

"""
    frink.orm
    ~~~~~~~~~~~~~
    ORM type functionality
"""

from fabric.colors import green, red, blue, cyan, magenta, yellow  # NOQA

import uuid
import logging
import rethinkdb as r
from inflection import tableize
from schematics.models import ModelMeta
from schematics.exceptions import ModelValidationError

from .errors import FrinkError, NotUniqueError
from .registry import model_registry
from .connection import rconnect


def get_log(extra=None):
    m = "{}.{}".format(__name__, extra) if extra else __name__
    return logging.getLogger(m)

log = get_log()


class InstanceLayerMixin(object):

    def save(self):
        """
            Save the current instance to the DB
        """
        with rconnect() as conn:
            try:
                self.validate()
            except ModelValidationError as e:
                print(red(e))
                return False
            else:
                # If this is a new unsaved object, it'll likely have an
                # id of None, which RethinkDB won't like. So if it's None,
                # generate a UUID for it. If the save fails, we should re-set
                # it to None.
                if self.id is None:
                    self.id = str(uuid.uuid4())
                    log.info(self.id)

                try:
                    rv = r.db(self._db).table(self._table).insert(
                        self.to_primitive(),
                        conflict="replace"
                    ).run(conn)
                    # Returns something like this:
                    # {
                    #   u'errors': 0,
                    #   u'deleted': 0,
                    #   u'generated_keys': [u'dd8ad1bc-8609-4484-b6c4-ed96c72c03f2'],
                    #   u'unchanged': 0,
                    #   u'skipped': 0,
                    #   u'replaced': 0,
                    #   u'inserted': 1
                    # }
                    log.info(green(rv))
                except Exception as e:
                    log.warn(red(e))
                    self.id = None
                else:
                    return self

    def delete(self):
        """
            Delete the current instance from the DB.
        """
        with rconnect() as conn:
            # Can't delete an object without an ID.
            if self.id is None:
                raise FrinkError
            else:
                if isinstance(self.id, uuid.UUID):
                    self.id = str(self.id)

                try:
                    rv = r.db(
                        self._db
                    ).table(
                        self._table
                    ).get(
                        self.id
                    ).delete().run(conn)
                    log.info(green(rv))
                except Exception as e:
                    raise
                    log.warn(red(e))
                else:
                    return True
        return False


class ORMMeta(ModelMeta):

    instance = None

    def __new__(cls, name, bases, dct):
        if name != "BaseModel":
            # We have a model class
            cls._table = tableize(name)
            super_new = super(ORMMeta, cls).__new__
            new_class = super_new(cls, name, bases, dct)
            cls._model = new_class
            cls._orm = ORMLayer(cls._table, cls._model)
            setattr(new_class, 'query', cls._orm)
            setattr(new_class, '_table', cls._table)
            # register the model
            model_registry.add(name, new_class, cls)

        return new_class


class ORMLayer(object):

    def __init__(self, table, model):
        self._model = model
        self._table = table
        print('query init {}'.format(self._table))

    def get(self, id):
        """
            Get a single instance by pk id.

            :param id: The UUID of the instance you want to retrieve.

        """
        with rconnect() as conn:
            if id is None:
                raise ValueError

            if isinstance(id, uuid.UUID):
                id = str(id)

            if type(id) != str and type(id) != unicode:
                raise ValueError

            try:
                rv = self._base().get(id).run(conn)
            except Exception as e:
                print(red(e))
                raise
            if rv is not None:
                return self._model(rv)

            return None

    def filter(self, order_by=None, limit=0, **kwargs):
        """
            Fetch a list of instances.

            :param order_by: column on which to order the results. \
            To change the sort, prepend with < or >.
            :param limit: How many rows to fetch.
            :param kwargs: keyword args on which to filter, column=value

        """
        with rconnect() as conn:
            print(magenta(kwargs))
            if len(kwargs) == 0:
                raise ValueError

            try:
                query = self._base()
                if order_by is not None:
                    query = self._order_by(query, order_by)

                rv = query.filter(kwargs).run(conn)

                if limit > 0:
                    query = self._limit(query, limit)

            except Exception as e:
                print(red(e))
                raise
            else:
                data = [self._model(_) for _ in rv]
                return data

    def first(self, order_by=None, **kwargs):
        """
            Fetch the first item that matches your filter.

            :param order_by: column on which to order the results. \
            To change the sort, prepend with < or >.
            :param kwargs: keyword args on which to filter, column=value

        """
        with rconnect() as conn:
            if len(kwargs) == 0:
                raise ValueError

            try:
                query = self._base()
                if order_by is not None:
                    query = self._order_by(query, order_by)

                # NOTE: Always filter before limiting
                query = query.filter(kwargs)
                query = self._limit(query, 1)
                rv = query.run(conn)
            except Exception as e:
                print(red(e))
                raise
            else:
                data = [self._model(_) for _ in rv]
                try:
                    return data[0]
                except IndexError:
                    return None

    def find_by(self, column=None, value=None, order_by=None, limit=0):
        """
            Find all items that matches your a column/value.

            :param column: column to search.
            :param value: value to look for in `column`.
            :param limit: How many rows to fetch.
            :param order_by: column on which to order the results. \
            To change the sort, prepend with < or >.

        """
        with rconnect() as conn:
            if column is None or value is None:
                raise ValueError("You need to supply both a column and a value")

            try:
                query = self._base()
                if order_by is not None:
                    query = self._order_by(query, order_by)
                if limit > 0:
                    query = self._limit(query, limit)

                rv = query.filter({column: value}).run(conn)
            except Exception as e:
                print(red(e))
                raise
            else:
                data = [self._model(_) for _ in rv]
                return data

    def get_by(self, column=None, value=None):
        """
            Find one item that matches your a column/value. Raises `NotUniqueError` if
            it finds more than one.

            :param column: column to search.
            :param value: value to look for in `column`.
            :param limit: How many rows to fetch.
            :param order_by: column on which to order the results. \
            To change the sort, prepend with < or >.

        """
        with rconnect() as conn:
            if column is None or value is None:
                raise ValueError("You need to supply both a column and a value")

            try:
                query = self._base()
                rv = query.filter({column: value}).run(conn)
            except Exception as e:
                print(red(e))
                raise
            else:
                data = [self._model(_) for _ in rv]
                if len(data) > 1:
                    raise NotUniqueError('Found more than one object matching the query')
                else:
                    try:
                        return data[0]
                    except IndexError:
                        return None

    def all(self, order_by=None, limit=0):
        """
            Fetch all items.

            :param limit: How many rows to fetch.
            :param order_by: column on which to order the results. \
            To change the sort, prepend with < or >.

        """
        with rconnect() as conn:
            try:
                query = self._base()
                if order_by is not None:
                    query = self._order_by(query, order_by)
                if limit > 0:
                    query = self._limit(query, limit)

                rv = query.run(conn)
            except Exception as e:
                print(red(e))
                raise
            else:
                data = [self._model(_) for _ in rv]
                return data

    def _limit(self, query, limit):
        with rconnect() as conn:
            try:
                rv = query.limit(limit)
            except Exception as e:
                print(red(e))
                raise
            else:
                return rv

    def _order_by(self, query, column):
        with rconnect() as conn:
            if column.startswith('>'):
                column = column[1:]
                index = r.desc(column[1:])
            elif column.startswith('<'):
                column = column[1:]
                index = r.asc(column[1:])
            else:
                index = column

            try:
                rv = query.order_by(index)
            except Exception as e:
                print(red(e))
                raise
            else:
                return rv

    def _base(self):
        return r.db(self._db).table(self._table)
