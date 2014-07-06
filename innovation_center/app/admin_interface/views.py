from flask.ext.admin import BaseView, expose
from flask.ext.login import current_user

class AdminViews(BaseView):
    def is_accessible(self):
        return current_user.is_admin()

    @expose('/')
    def index(self):
        return self.render('admin/index.html')