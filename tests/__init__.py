from flask.ext.testing import TestCase as Base

from innovation_center.app import create_app
from innovation_center.app.extensions import db
from innovation_center.app.auth.models import User
from innovation_center.app.auth.roles import ADMIN, USER

class TestCase(Base):
    def create_app(self):
        """ create the application for flask-testing """
        return create_app('TESTING')

    def init_data(self):
        """ Put some generic info in the database """
        new_user = User(
            username=u'jackdaw',
            email=u'jackdaw@corvid.com',
            password=u'the_jackdaw',
            role_code=USER,
            first_name=u'jackdaw',
            last_name=u'corvid'
        )
        admin = User(
            username=u'crow',
            email=u'crow@corvid.com',
            password=u'a_cat_among_men',
            role_code=ADMIN,
            first_name=u'crow',
            last_name=u'corvid'
        )
        db.session.add(new_user)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        db.create_all()
        self.init_data()

    def tearDown(self):
        db.drop_all()

    def login(self, email, password):
        credentials = dict(
            email=email,
            password=password
        )
        resp = self.client.post('/user/login', data=credentials, follow_redirects=True)
        return resp