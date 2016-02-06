# coding: utf8
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask.ext.login import login_user
from .. import db
from ..models import User
from ..forms.user import LoginForm

bp = Blueprint('user', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()

    status = 1
    data = ['form']
    if form.validate_on_submit():
        print '>>> 2', form.email.data, form.password.data, form.remember_me.data
        user = User.query.filter(User.email == form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return jsonify({
                'status': 0,
                'data': data
            })

    data.append({'password': u'用户名或密码错误'})
    return jsonify({
        'status': status,
        'data': data
    })


@bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    mail = request.form.get('mail')
    password = request.form.get('password')

    status = 0
    data = {}
    if mail or name:
        from sqlalchemy import or_
        user = User.query.filter(or_(User.email == mail, User.name == name)).first()
        if user:
            status = 1
            data = {0: 'form', 1: {'mail': u'mail或用户名已存在'}}
            return jsonify({
                'status': status,
                'data': [data],
                'message': u'注册失败'
            })

    if password:
        user = User(email=mail, password=password, name=name)
        db.session.add(user)
        db.session.commit()

    return jsonify({
        'status': status,
        'data': [data],
        'message': u'注册成功'
    })

    return render_template('layout.html')
