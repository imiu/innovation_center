from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime
from .extensions import db, login_manager
from .constants import USER_ROLE, ADMIN, USER
from flask.ext.login import UserMixin, AnonymousUserMixin

@login_manager.user_loader
def load_user(identification):
    return User.query.get(int(identification))


class User(db.Model, UserMixin):
    """ a user of the application """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(24), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    articles = db.relationship('NewsArticle', backref='author', lazy='dynamic')

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
            hashlib.md5(self.email.encode('utf-8')).hexdigest(), size, default, rating
        )

    # the user's role
    role_code = db.Column(db.SmallInteger, default=USER, nullable=False)
    @property
    def role(self):
        return USER_ROLE[self.role_code]

    def is_admin(self):
        return self.role_code == ADMIN

    @staticmethod
    def add_fake_users(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py as f

        seed()
        for i in range(count):
            u = User(
                email=f.internet.email_address(),
                username=f.internet.user_name(True),
                password=f.lorem_ipsum.word(),
                first_name=f.name.first_name(),
                last_name=f.name.last_name()
            )
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User {} (email={})>'.format(self.username, self.email)


class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512))
    body = db.Column(db.Text())
    time_written = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def populate_news(count=100):
        from random import seed, randint
        import forgery_py as f

        seed()
        for i in range(count):
            u = User.query.all()[randint(0, User.query.count() - 1)]

            article = NewsArticle(
                title=f.lorem_ipsum.sentences(1),
                body=f.lorem_ipsum.paragraphs(quantity=randint(5, 20), html=True, sentences_quantity=randint(7,25)),
                time_written=f.date.date(past=True, max_delta=20),
                author=u
            )
            db.session.add(article)
            db.session.commit()