#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()], description=u'hello@xxx.com')
    password = PasswordField(u'密码', validators=[DataRequired()], description=u'密码')
    remember_me = BooleanField(u'记住登录状态')
    submit = SubmitField(u'登录')


class RegisterForm(Form):
    username = StringField(u'用户名', validators=[InputRequired(), Length(1, 64)], description=u'字母、数字等，用户名唯一')
    email = StringField(u'邮箱', validators=[InputRequired(), Length(1, 64),
                                           Email()], description=u'hello@xxx.com')
    password = PasswordField(u'密码', validators=[InputRequired(), Length(1, 64)], description=u'不少于 6 位')
    submit = SubmitField(u'注册')
