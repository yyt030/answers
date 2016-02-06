#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                           Email()], description=u'hello@xxx.com')
    password = PasswordField(u'密码', validators=[DataRequired()], description=u'密码')
    remember_me = BooleanField(u'记住登录状态')
    submit = SubmitField(u'登录')
