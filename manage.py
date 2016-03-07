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
    """clear cache"""
    cache.init_app(app)
    with app.app_context():
        cache.clear()


@manager.command
def rungevent():
    """run http server in gevent"""
    from gevent.wsgi import WSGIServer

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()


@manager.command
def runtornado():
    """run http server in Tornado"""
    from tornado.options import define, options
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    define("port", default=5000, help="run on the given port", type=int)
    define("develop", default=True, help="develop environment", type=bool)

    options.parse_command_line()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(options.port)
    print "visit at", "http://127.0.0.1:%s" % options.port
    IOLoop.instance().start()


if __name__ == '__main__':
    manager.run()
