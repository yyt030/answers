#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from datetime import datetime

from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False, unique=False, index=True)
    email = db.Column(db.String(15), nullable=False, unique=False)
    password = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    questions = db.relationship('Question', backref='asker', lazy='dynamic')
    answers = db.relationship('Answer', backref='answerer', lazy='dynamic')
