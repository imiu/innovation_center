import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig(object):
    PROJECT = 'BURRDY'
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(_basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    RESULTS_PER_PAGE = 10
    LOG_FOLDER = os.path.join(_basedir, 'app.log')

    if not os.path.exists(os.path.dirname(LOG_FOLDER)):
        os.makedirs(LOG_FOLDER)


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(_basedir, 'data.sqlite')


config = {
    'DEFAULT': DefaultConfig,
    'DEVELOPMENT': DevelopmentConfig,
    'TESTING': TestingConfig,
    'PRODUCTION': ProductionConfig
}