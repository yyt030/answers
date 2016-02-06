#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template
from ..models import User, Question, Answer, Tag
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def questions():
    login_form = LoginForm()
    register_form = RegisterForm()
    users = User.query.all()
    questions = Question.query.all()
    answers = Answer.query.all()
    tags = Tag.query.all()
    # return render_template('layout.html', login_form=login_form, register_form=register_form)
    return render_template('layout.html', login_form=login_form, register_form=register_form)
