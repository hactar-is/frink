# -*- coding: utf-8 -*-

"""
    frink.tests.app.settings
    ~~~~~~~~~~~~~
    config objects for the test environment
"""


class Config(object):

    # MailJet
    MJ_APIKEY_PUBLIC = ''
    MJ_APIKEY_PRIVATE = ''

    RETHINKDB_AUTH = ''

    RDB_HOST = '127.0.0.1'
    RDB_PORT = 28015
    RDB_DB = 'frink_tests'

    SECRET_KEY = "M~DsRa1jhRGUxE?REfCdUs?Y4CPtI7wxHrSL3vXxG9TVg1eL5p"

    SESSION_COOKIE_NAME = 'frink_session'

    # Flask-security
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_REGISTER_VIEW = '/registered'
    SECURITY_POST_CONFIRM_VIEW = '/'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'QFAsMrN9.JTkn6iAeUa2iDH73k7en,qE@UeXhbSYkU3YHTgjfN'
    SECURITY_CONFIRM_SALT = 'QbUpDaeNVYUkib1mc34ZgV|e5zCsPK_SmFpf19Jl4omzO+HyWQ'
    SECURITY_RESET_SALT = 'IX3E>[fmYnowiWnXuAS7YwOEr$gyDp3wlLNbm6vIa7mXsE8QU2'
    SECURITY_LOGIN_SALT = 'IyR{9gAk1MIoYQPVB6QxOvxR6oc_uyw8bjSzCHvXQftp2~KZ4L'
    SECURITY_EMAIL_SENDER = 'test@foo.com'
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = True
    SECURITY_EMAIL_SUBJECT_REGISTER = "Welcome"
    SECURITY_EMAIL_SUBJECT_PASSWORDLESS = "Login instructions"
    SECURITY_EMAIL_SUBJECT_PASSWORD_SET = "Login instructions"
    SECURITY_LOGIN_DISABLED = False

    # i18n
    LANGUAGES = {
        'en': 'English'
    }

    # Flask-mail settings
    MAIL_ENABLED = True
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    DEFAULT_MAIL_SENDER = 'test@foo.com'
    DEFAULT_MAIL_REPLY = 'test@foo.com'

    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
