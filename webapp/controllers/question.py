#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from ..forms.user import LoginForm, RegisterForm
from ..models import User, Question, Answer, Tag

bp = Blueprint('question', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/<string:act>', methods=['GET', 'POST'])
def index(act=None):
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    page = request.args.get('page', 1, type=int)

    if act == 'hottest':
        pagination = query.order_by(Question.view_num.desc()).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        questions = pagination.items
    elif act == 'unanswered':
        from sqlalchemy import exists
        query = query.filter(~exists().where(Question.id == Answer.question_id))
        pagination = query.order_by(Question.create_time.desc()).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        questions = pagination.items
    else:
        pagination = query.order_by(Question.create_time.desc()).paginate(
                page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                error_out=False)
        questions = pagination.items

    # tags
    tags = Tag.query.order_by(Tag.create_time.desc()).limit(15)

    return render_template('layout.html', login_form=login_form, register_form=register_form,
                           pagination=pagination, questions=questions, tags=tags, act=act)
