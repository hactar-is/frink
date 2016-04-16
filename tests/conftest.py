# -*- coding: utf-8 -*-

"""
    frink.tests.conftest
    ~~~~~~~~~~~~~
    frink pytest config and fixtures
"""

import pytest

from app.factory import create_app

from frink.registry import model_registry

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app('frink_test')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    model_registry.drop_tables()
    ctx.pop()
