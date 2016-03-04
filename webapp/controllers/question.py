#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, request, redirect, url_for
from flask.ext.login import current_user, login_required
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question, Answer

from .. import db, cache

bp = Blueprint('question', __name__)


@bp.route('/')
@bp.route('/<int:question_id>')
@cache.cached()
def questions(question_id=None):
    """问题详情"""
    if not question_id:
        return redirect(url_for('site.index'))
    question = Question.query.get_or_404(question_id)
    login_form = LoginForm()
    register_form = RegisterForm()

    question.view_num += 1
    db.session.add(question)
    db.session.commit()

    return render_template('question.html', question=question, login_form=login_form,
                           register_form=register_form)


@bp.route('/<int:question_id>/answers/add', methods=['GET', 'POST'])
@login_required
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
