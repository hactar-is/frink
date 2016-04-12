# -*- coding: utf-8 -*-

from app.models import User, Role
from frink.registry import model_registry


def test_mr_contains_user(app):
    assert 'User' in model_registry._models


def test_mr_contains_role(app):
    assert 'Role' in model_registry._models
