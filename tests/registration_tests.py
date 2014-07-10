from tests import TestCase
import sys

from innovation_center.app.models import User
from innovation_center.app.auth.forms import RegistrationForm
from innovation_center.app.extensions import db

class RegistrationTests(TestCase):

    def test_page_exists(self):
        resp = self.client.get('/user/register')
        self.assertEquals(resp.status_code, 200)

    def test_valid_registration(self):
        """ test a user registering for the first time, valid """
        r = dict(
            email='magpie@corvid.com',
            username='crow',
            password='I_do_not_caw',
            confirm_password='I_do_not_caw',
            first_name='magpie',
            last_name='corvid'
        )
        resp = self.client.post('/user/register', data=r, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)