# coding: utf8
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask.ext.login import login_user
from .. import db
from ..models import User

bp = Blueprint('user', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    remember = request.form.get('remember')

    status = 0
    data = None
    message = None
    if mail:
        user = User.query.filter(User.email == mail).first()
        if not user:
            status = 1
            data = ['form', {'mail': u'mail不存在'}]
    if password:
        user = User.query.filter(User.email == mail, User.password == password).first()
        if not user:
            status = 1
            data = ['form', {'password': u'用户名或密码不正确'}]
        else:
            data = ['form', {'password': u'用户名或密码不正确'}]
            login_user(user, remember)
            return redirect(url_for('site.questions'))

    return jsonify({
        'status': status,
        'data': data,
        'message': message
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
