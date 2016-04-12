# -*- coding: utf-8 -*-

"""
    frink.tests.conftest
    ~~~~~~~~~~~~~
    frink pytest config and fixtures
"""
import os

import pytest

import rethinkdb as r
from app.factory import create_app
from app.core import db as _db

from frink.connection import rconnect


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app('frink_test')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app

    yield _db

    # _db.drop_all(app)