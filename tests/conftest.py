# -*- coding: utf-8 -*-

"""
    frink.tests.conftest
    ~~~~~~~~~~~~~~~~~~~~
    frink pytest config and fixtures
"""

import pytest  # NOQA
import logging
from frink import frink
from frink.registry import model_registry


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.yield_fixture(scope='session')
def base():

    frink.init(db="frinktests")

    yield frink

    model_registry.drop_tables()
