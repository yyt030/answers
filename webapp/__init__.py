# coding: utf8

from config import config
from flask import Flask, g
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    from .utils.account import get_current_user
    @app.before_request
    def before_request():
        g.user = get_current_user()

    from .controllers import question, site, user
    from .api import user as user_api

    app.register_blueprint(question.bp, url_prefix='/q')
    app.register_blueprint(user.bp, url_prefix='/user')
    app.register_blueprint(user_api.bp, url_prefix='/api')
    app.register_blueprint(site.bp, url_prefix='')

    return app
