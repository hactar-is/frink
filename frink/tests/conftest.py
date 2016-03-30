# -*- coding: utf-8 -*-

"""
    frink.tests.conftest
    ~~~~~~~~~~~~~
    frink pytest config and fixtures
"""
import os

import pytest

from app.factory import create_app


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app('frink_test')
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()
