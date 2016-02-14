#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, request
from flask.ext.login import current_user
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question
from ..utils.permissions import require_user

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
@require_user
def answers_add(question_id):
    """问题详情"""
    question = Question.query.get_or_404(question_id)
    login_form = LoginForm()
    register_form = RegisterForm()
    answer_data = request.form.get('answer_data')
    print '>>>', answer_data, current_user

    return render_template('question.html', question=question, login_form=login_form,
                           register_form=register_form)
