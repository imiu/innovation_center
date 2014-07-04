from . import TestCase
from flask import current_app
from innovation_center.app.extensions import db
from innovation_center.app.user.models import User

class SetupTest(TestCase):

    def test_app_exists(self):
        self.assertTrue(current_app is not None)

    def test_config_type(self):
        self.assertTrue('TESTING' in current_app.config)

    def test_db_populated(self):
        valid_user = User.query.filter_by(email="crow@corvid.com").first()
        self.assertTrue(valid_user is not None)
        invalid = User.query.filter_by(email="invalid@email.com").first()
        self.assertTrue(invalid is None)