# -*- coding: utf-8 -*-


def test_dev_config(app):
    assert app.config['DEBUG'] is True
