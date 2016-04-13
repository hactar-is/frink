# -*- coding: utf-8 -*-


def test_dev_config(app):
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is True
    assert app.config['CSRF_ENABLED'] is False
    assert app.config['WTF_CSRF_ENABLED'] is False


def test_db_config(app):
    assert app.config['RDB_HOST'] == '127.0.0.1'
    assert app.config['RDB_PORT'] == 28015
    assert app.config['RDB_DB'] == 'frink_tests'


def test_request(app, client):
    rv = client.get('/ping/')
    assert rv.status_code == 200
