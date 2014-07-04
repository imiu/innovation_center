from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime
from ..extensions import db, login_manager
from .roles import USER_ROLE, ADMIN, USER
from flask.ext.login import UserMixin

@login_manager.user_loader
def load_user(identification):
    return User.query.get(id(identification))


class User(db.Model, UserMixin):
    """ a user of the application """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(24), unique=True)
    email = db.Column(db.String(128), unique=True)
    joined = db.Column(db.DateTime, default=datetime.utcnow)

    # The password
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        """ don't allow people to read password """
        raise AttributeError('the password is an unreadable attribute')

    @password.setter
    def password(self, password):
        """ set the password to a hash """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """ check that the password matches the decoded hash """
        return check_password_hash(self.password_hash, password)

    def gravatar(self, size=128, default='identicon', rating='g'):
        """ user avatar, using gravatar """
        return 'http://www.gravatar.com/avatar/{}?s={}&d={}&r={}'.format(
            md5(self.email.encode('utf-8')).hexdigest(), size, rating, default
        )

    # the user's role
    role_code = db.Column(db.SmallInteger, default=USER, nullable=False)

    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    def __repr__(self):
        return '<User {} (email={})>'.format(self.username, self.email)