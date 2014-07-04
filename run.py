from innovation_center.app import create_app
from innovation_center.app.extensions import db
from innovation_center.app.user.models import User
from innovation_center.app.user.roles import ADMIN
from flask.ext.script import Manager, Shell

app = create_app('DEVELOPMENT')
manager = Manager(app)

@manager.command
def initdb():
    db.drop_all()
    db.create_all()

    admin = User(
        first_name='Alex',
        last_name='Frazer',
        email='dreadsin@gmail.com',
        role_code=ADMIN,
        username='admin',
        password='a-cat-among-men'
    )
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    manager.run()