import os
import sys
import logging
from flask import Flask
from flask import jsonify
from logging import Formatter
from logging.handlers import RotatingFileHandler

from .models import User
from .extensions import db, login_manager, bootstrap, admin, moment
from .admin_interface.views import AdminViews, UserViews
from ..config import config as c


def create_app(environment='DEFAULT'):
    """ create an instance of the flask application """
    app = Flask(__name__)
    app.config.from_object(c[environment])

    configure_extensions(app)
    configure_logger(app)

    from .root import root
    from .auth import auth
    app.register_blueprint(root)
    app.register_blueprint(auth, url_prefix='/user')

    return app


def configure_extensions(app):
    """ loads the flask extensions onto the application """
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.session_protected = 'strong'
    login_manager.login_view = 'auth.login'

    bootstrap.init_app(app)

    moment.init_app(app)


def configure_logger(app):
    """ put a logger on the application """
    if app.testing or app.debug:
        return

    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setLevel(logging.WARNING)
    flask_log = RotatingFileHandler(
        os.path.join(app.config['LOG_FOLDER'], 'flask.log'),
        maxBytes=10000,
        backupCount=2
    )
    flask_log.setLevel(logging.WARNING)
    flask_log.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(flask_log)
    app.logger.addHandler(stream_handler)
    