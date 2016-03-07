#!/usr/bin/env python
# coding: utf8
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from webapp import create_app, db, cache
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def init_data():
    from webapp.models.user import User
    from webapp.models.question import Question, Tag, Answer
    # Role.insert_roles()

    User.generate_fake(100)
    Tag.generate_fake(20)
    Question.generate_fake(1000)
    Answer.generate_fake(100)


@manager.command
def clear_cache():
    cache.init_app(app)
    with app.app_context():
        cache.clear()


@manager.command
def rungevent():
    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()


if __name__ == '__main__':
    manager.run()
