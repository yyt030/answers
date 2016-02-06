#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from .. import db
from .user import User


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    vote_num = db.Column(db.SmallInteger, nullable=False, default=0)
    view_num = db.Column(db.SmallInteger, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    answers = db.relationship('Answer', backref='question', lazy='dynamic')

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            print '>>>', u
            p = Question(body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                         create_time=forgery_py.date.date(True),
                         title=forgery_py.name.job_title(),
                         asker=u)
            db.session.add(p)
            db.session.commit()


# 问题 和 标签　的many to many 关系
question_tag = db.Table('question_tag',
                        db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), index=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)

    questions = db.relationship('Question', secondary=question_tag,
                                backref=db.backref('tags', lazy='dynamic'), lazy='dynamic')
    create_time = db.Column(db.DateTime, nullable=False,default=datetime.now)