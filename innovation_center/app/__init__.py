import os
import logging
from flask import Flask
from flask import jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from logging import Formatter
from logging.handlers import RotatingFileHandler
from .extensions import flask_ext
from ..config import config as c


def create_app(environment='DEFAULT'):
    """ create an instance of the flask application """
    app = Flask(__name__)
    app.config.from_object(c[environment])

    configure_extensions(app)
    configure_logger(app)

    from .root import root
    from .user import user
    app.register_blueprint(root)
    app.register_blueprint(user, url_prefix='/user')

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_error_json

    return app


def configure_extensions(app):
    """ loads the flask extensions onto the application """
    for extension in flask_ext:
        extension.init_app(app)


def configure_logger(app):
    """ put a logger on the application """
    if app.testing or app.debug:
        return
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


def make_error_json(ex):
    """ creates a json out of an error """
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.code
        if isinstance(ex, HTTPException)
        else 500
    )