from . import TestCase
from innovation_center.app.auth.models import User
from innovation_center.app.auth.forms import RegistrationForm
from innovation_center.app.extensions import db

class RegistrationTest(TestCase):
    def test_new_user_registration(self):
        self.client.get('/user/register')
        form = RegistrationForm(
            email=u'crow@crow.com',
            first_name=u'Alex',
            last_name=u'Frazer',
            username=u'corvid',
            password=u'fake_password',
            confirm_password=u'fake_password'
        )
        self.assertTrue(form.validate())