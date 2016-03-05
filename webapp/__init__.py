# coding: utf8

from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()
cache = Cache(config={'CACHE_TYPE': 'redis'})

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'user_api.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

    from .controllers import question, site, user
    from .api import user as user_api

    app.register_blueprint(question.bp, url_prefix='/q')
    app.register_blueprint(user_api.bp, url_prefix='/api')
    app.register_blueprint(site.bp, url_prefix='')

    return app
