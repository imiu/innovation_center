import unittest
from innovation_center.app import create_app
from innovation_center.app.extensions import db
from innovation_center.app.user.models import User

class TestCase(unittest.TestCase):
    def init_db(self):
        u = User(
            first_name="Alex",
            last_name="Frazer",
            password="password",
            username="crow",
            email="email@email.com"
        )
        admin = User(
            first_name="Alex",
            last_name="Frazer",
            password="password",
            username="admin_crow",
            email="crow@corvid.com"
        )
        db.session.add(u)
        db.session.add(admin)
        db.session.commit()

    def setUp(self):
        self.app = create_app('TESTING')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        db.create_all()
        self.init_db()

    def tearDown(self):
        db.drop_all()
        self.ctx.pop()
