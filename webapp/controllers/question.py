#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, request
from flask.ext.login import current_user
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question
from ..models.answer import Answer
from ..utils.permissions import require_user

from .. import db

bp = Blueprint('question', __name__)


@bp.route('/<int:question_id>')
def questions(question_id):
    """问题详情"""
    question = Question.query.get_or_404(question_id)
    login_form = LoginForm()
    register_form = RegisterForm()

    return render_template('question.html', question=question, login_form=login_form,
                           register_form=register_form)


@bp.route('/<int:question_id>/answers/add', methods=['GET', 'POST'])
# @require_user
def answers_add(question_id):
    """问题详情"""
    question = Question.query.get_or_404(question_id)
    login_form = LoginForm()
    register_form = RegisterForm()
    answer_data = request.form.get('answer_data')
    if answer_data:
        answer = Answer(question_id=question_id, author_id=current_user.id,
                        title=answer_data[1:100], body=answer_data)
        db.session.add(answer)
        db.session.commit()

    return render_template('question.html', question=question, login_form=login_form,
                           register_form=register_form)
