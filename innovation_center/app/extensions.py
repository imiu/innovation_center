from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.login import LoginManager
login_manager = LoginManager()
login_manager.session_protected = 'strong'
login_manager.login_view = 'user.login'

from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap()

flask_ext = [
    db,
    login_manager,
    bootstrap
]