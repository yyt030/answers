#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from ..forms.user import LoginForm, RegisterForm
from ..models import User, Question, Answer, Tag

bp = Blueprint('question', __name__)


@bp.route('/<int:question_id>')
def questions(question_id):
    """问题详情"""
    question = Question.query.get_or_404(question_id)
    print '>>>'

    return render_template('question.html')
