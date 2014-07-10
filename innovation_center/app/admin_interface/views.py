from flask.ext.admin import BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask import url_for

class AdminViews(BaseView):
    def is_accessible(self):
        return current_user.is_admin()

    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class UserViews(ModelView):
    def is_accessible(self):
        return current_user.is_admin()

    column_list = ('username', 'email', 'role_code')

    def __init__(self, User, session, **kwargs):
        super(UserViews, self).__init__(User, session, **kwargs)