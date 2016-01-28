# coding: utf8

from flask import Flask
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from config import config

moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    moment.init_app(app)
    db.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)

    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    from .controllers import question, site
    app.register_blueprint(question.bp, url_prefix='/questions')
    app.register_blueprint(site.bp, url_prefix='')

    return app
