import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(_basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    LOG_FOLDER = os.path.join(_basedir, 'app.log')

    if not os.path.exists(os.path.dirname(LOG_FOLDER)):
        os.makedirs(LOG_FOLDER)


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

config = {
    'DEFAULT': DefaultConfig,
    'DEVELOPMENT': DevelopmentConfig,
    'TESTING': TestingConfig
}