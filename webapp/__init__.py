# coding: utf8

from config import config
from flask import Flask, render_template,g
from flask.ext.bootstrap import Bootstrap
from flask.ext.cache import Cache
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from .forms.user import LoginForm, RegisterForm

moment = Moment()
db = SQLAlchemy()
bootstrap = Bootstrap()
cache = Cache(config={'CACHE_TYPE': 'simple'})

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

    from .controllers import question, site, user, tag
    from .api import user as user_api

    app.register_blueprint(question.bp, url_prefix='/q')
    app.register_blueprint(tag.bp, url_prefix='/t')
    app.register_blueprint(user_api.bp, url_prefix='/api')
    app.register_blueprint(user.bp, url_prefix='/u')
    app.register_blueprint(site.bp, url_prefix='')

    register_error_handle(app)

    @app.before_request
    def before_request():
        g.login_form = LoginForm()
        g.register_form = RegisterForm()

    return app


def register_error_handle(app):
    """添加HTTP错误页面"""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('500.html'), 500
