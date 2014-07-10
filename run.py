from innovation_center.app import create_app
from innovation_center.app.extensions import db
from innovation_center.app.models import User, NewsArticle
from innovation_center.app.constants import ADMIN
from flask.ext.script import Manager, Shell

app = create_app('DEVELOPMENT')
manager = Manager(app)

@manager.command
def initdemo():
    db.drop_all()
    db.create_all()

    admin = User(
        first_name='Alex',
        last_name='Frazer',
        email='dreadsin@gmail.com',
        role_code=ADMIN,
        username='admin',
        password='password'
    )
    db.session.add(admin)
    db.session.commit()
    User.add_fake_users()
    NewsArticle.populate_news()

if __name__ == '__main__':
    manager.run()