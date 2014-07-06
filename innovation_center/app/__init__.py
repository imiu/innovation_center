import os
import logging
from flask import Flask
from flask import jsonify
from logging import Formatter
from logging.handlers import RotatingFileHandler
from .auth.models import User
from flask.ext.admin.contrib.sqla import ModelView
from .extensions import db, login_manager, bootstrap, admin
from .admin_interface.views import AdminViews
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
    login_manager.login_view = 'user.login'

    bootstrap.init_app(app)

    admin.init_app(app)
    init_admin_views(app, db)


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


def init_admin_views(app, db):
    """ gives flask-admin the views to use """
    admin.add_view(ModelView(User, db.session))