#!/usr/bin/env python
# coding: utf8
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from webapp import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def init_data():
    from webapp.models.user import Role
    from webapp.models.question import Question
    from webapp.models.answer import Answer
    #Role.insert_roles()

    #Question.generate_fake(100)

    Answer.generate_fake(100)


if __name__ == '__main__':
    manager.run()
