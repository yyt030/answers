#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template
from ..models import User, Question, Answer, Tag

bp = Blueprint('question', __name__)


@bp.route('/', methods=['GET', 'POST'])
def questions():
    users = User.query.all()
    questions = Question.query.all()
    answers = Answer.query.all()
    tags = Tag.query.all()
    print '>>>'
    return render_template('layout.html')
