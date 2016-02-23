# coding: utf8
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask.ext.login import login_user
from .. import db
from ..forms.user import LoginForm, RegisterForm
from ..models.user import User

from sqlalchemy import or_

bp = Blueprint('user_api', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')


@bp.route('/user/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.is_xhr:
        # ajax post
        rsp_json = {
            'status': 1,
        }
        if login_form.validate_on_submit():
            user = User.query.filter(User.email == login_form.email.data).first()
            if user is not None and user.verify_password(login_form.password.data):
                # 登录成功
                login_user(user, remember=login_form.remember_me.data)

                rsp_json['data'] = request.url_root
                rsp_json['status'] = 0
                rsp_json['message'] = ''
                return jsonify(rsp_json)
            else:
                rsp_json['data'] = ['form', {'password': u'用户名或密码错误'}]
                return jsonify(rsp_json)
        return render_template('_login.html', login_form=login_form, register_form=register_form)
    else:
        # html page submit
        if login_form.validate_on_submit():
            user = User.query.filter(User.email == login_form.email.data).first()
            if user is not None and user.verify_password(login_form.password.data):
                # 登录成功
                login_user(user, remember=True)
                return redirect(url_for('site.index'))
            flash(u'用户名或密码错误')
        return render_template('user/login.html', login_form=login_form,
                               register_form=register_form, login_type='page')


@bp.route('/user/register', methods=['POST'])
def register():
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.is_xhr:
        # ajax post
        rsp_json = {
            'status': 1
        }

        if register_form.validate_on_submit():
            user = User.query.filter(User.username == register_form.username.data).first()
            if user:
                # 注册失败
                rsp_json['data'] = ['form', {'password': u'用户名已注册'}]
                return jsonify(rsp_json)
            else:
                # 注册成功
                user = User(username=register_form.username.data,
                            password=register_form.password.data,
                            email=register_form.email.data)
                db.session.add(user)
                db.session.commit()

                rsp_json['data'] = request.url_root
                rsp_json['status'] = 0
                rsp_json['message'] = ''
                return jsonify(rsp_json)
        return render_template('_login.html', login_form=login_form, register_form=register_form)
    else:
        # html page submit
        if register_form.validate_on_submit():
            user = User.query.filter(or_(
                    User.email == register_form.email.data,
                    User.username == register_form.username.data
            )).first()
            if user:
                flash(u'注册失败，用户名或邮箱已存在')
            else:
                # 注册成功
                user = User(username=register_form.username.data,
                            password=register_form.password.data,
                            email=register_form.email.data)
                db.session.add(user)
                db.session.commit()
                flash(u'注册成功')
        return render_template('user/login.html', login_form=login_form,
                               register_form=register_form, login_type='page')
