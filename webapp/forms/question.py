#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, Email


class QuestionForm(Form):
    title = StringField(u'标题', validators=[InputRequired(), Length(1, 64)],
                        description=u'一句话说清问题，用问号结尾')
    tags = StringField(u'标签', validators=[InputRequired(), Length(10, 64)],
                       description=u'至少1个，最多5个，如：php 可使用逗号,分号;分隔')
    # body = PasswordField(u'问题详细描述', validators=[InputRequired()],s
    #                      description=u'1. 描述你的问题 \n2. 贴上相关代码 3. 贴上报错信息 4. 贴上相关截图 5. 已经尝试过哪些方法仍然没解决（附上相关链接）')
    submit = SubmitField(u'发布问题')
