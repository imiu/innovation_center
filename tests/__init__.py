import unittest

from innovation_center.app import create_app
from innovation_center.app.extensions import db
from innovation_center.app.models import User
from innovation_center.app.constants import ADMIN, USER

class TestCase(unittest.TestCase):

    def init_data(self):
        """ Put some generic info in the database
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
        db.session.commit()"""

    def setUp(self):
        self.app = create_app('TESTING')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        db.create_all()
        self.init_data()

    def tearDown(self):
        self.ctx.pop()
        db.session.remove()
        db.drop_all()