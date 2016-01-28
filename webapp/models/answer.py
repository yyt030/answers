#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from .. import db


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)

    like_num = db.Column(db.SmallInteger, nullable=False, default=0)
    hate_num = db.Column(db.SmallInteger, nullable=False, default=0)

    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    author_id = db.Column(db.ForeignKey('user.id'))

    question_id = db.Column(db.ForeignKey('question.id'))
