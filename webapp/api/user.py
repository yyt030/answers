# coding: utf8
from flask import Blueprint, render_template, jsonify
from flask.ext.login import login_user
from .. import db
from ..forms.user import LoginForm, RegisterForm
from ..models.user import User

bp = Blueprint('user_api', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    register_form = RegisterForm()

    rsp_json = {
        'status': 1,
        'data': ['form']
    }

    if form.validate_on_submit():
        print '>>> 2', form.email.data, form.password.data, form.remember_me.data
        user = User.query.filter(User.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            rsp_json['status'] = 0
            return jsonify(rsp_json)
        else:
            rsp_json['data'].append({'password': u'用户名或密码错误'})
            return jsonify(rsp_json)
    return render_template('_login.html', login_form=form, register_form=register_form)


@bp.route('/register', methods=['POST'])
def register():
    form = RegisterForm()

    rsp_json = {
        'status': 1,
        'data': ['form']
    }

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        print '>>>', user, form.username.data, form.password.data, type(form.username.data)
        if user:
            rsp_json['data'].append({'username': u'用户名已注册'})
            return jsonify(rsp_json)
        else:
            user = User(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            rsp_json['status'] = 0
    rsp_json['data'].append({'email': u'注册失败'})
    return jsonify(rsp_json)