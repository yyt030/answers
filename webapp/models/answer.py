#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from .. import db
from .user import User
from .question import Question


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean, default=True)

    like_num = db.Column(db.SmallInteger, nullable=False, default=0)
    hate_num = db.Column(db.SmallInteger, nullable=False, default=0)

    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            q = Question.query.offset(randint(0, user_count - 1)).first()
            p = Answer(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                       create_time=forgery_py.date.date(True),
                       title=forgery_py.name.job_title(),
                       like_num=randint(1, 10), hate_num=randint(1, 10),
                       question_id=q.id, author_id=u.id)
            db.session.add(p)
            db.session.commit()
