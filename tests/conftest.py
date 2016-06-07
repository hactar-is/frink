# -*- coding: utf-8 -*-

"""
    frink.tests.conftest
    ~~~~~~~~~~~~~~~~~~~~
    frink pytest config and fixtures
"""

import pytest  # NOQA
import logging
from frink import frink


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


frink.init(db="frinktests")
