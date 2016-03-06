#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from bs4 import BeautifulSoup
from .user import User
from .. import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), index=True, nullable=False)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text, nullable=False)
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
        tag_count = Tag.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            t = Tag.query.offset(randint(0, tag_count - 1)).first()
            print '>>>', u
            q = Question(body_html=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                         create_time=forgery_py.date.date(True),
                         title=forgery_py.name.job_title(),
                         asker=u)
            db.session.add(q)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body = BeautifulSoup(value, 'html5lib').get_text()


db.event.listen(Question.body_html, 'set', Question.on_changed_body)

# 问题 和 标签　的many to many 关系
question_tag = db.Table('question_tag',
                        db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    __table_args__ = (db.UniqueConstraint('name', 'category', name='u_idx_name_01'),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), index=True, nullable=False)
    category = db.Column(db.String(20))

    questions = db.relationship('Question', secondary=question_tag,
                                backref=db.backref('tags', lazy='dynamic'), lazy='dynamic')
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in xrange(count):
            t = Tag(name=forgery_py.name.full_name(), category=forgery_py.name.title())
            db.session.add(t)
        db.session.commit()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), index=True, nullable=False)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text, nullable=False)
    disabled = db.Column(db.Boolean, default=True)

    vote_num = db.Column(db.SmallInteger, nullable=False, default=0)

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
            p = Answer(body_html=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                       create_time=forgery_py.date.date(True),
                       title=forgery_py.name.job_title(),
                       like_num=randint(1, 10), hate_num=randint(1, 10),
                       question_id=q.id, author_id=u.id)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        target.body = BeautifulSoup(value, 'html5lib').get_text()


db.event.listen(Answer.body_html, 'set', Answer.on_changed_body)
