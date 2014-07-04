import unittest
from flask import current_app
from innovation_center.app import create_app

class SetupTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TESTING')
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_app_created(self):
        self.assertTrue(current_app is not None)