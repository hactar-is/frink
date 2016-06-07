# -*- coding: utf-8 -*-

from app.models import User, Role
from frink.registry import model_registry


def test_mr_contains_user():
    assert 'User' in model_registry._models


def test_mr_contains_role():
    assert 'Role' in model_registry._models


def test_models_have_db_ref():
    assert hasattr(Role, '_db')
