#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from ..models import User, Question, Answer, Tag
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('.questions'))


@bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')

    return redirect(url_for('.index', q=q))


@bp.route('/login', methods=['GET'])
def login():
    return redirect(url_for('.index'))


@bp.route('/tags', methods=['GET'])
def tags():
    return redirect(url_for('.index'))


@bp.route('/tour')
def tour():
    return redirect(url_for('.index'))


@bp.route('/questions', methods=['GET', 'POST'])
@bp.route('/questions/<string:act>', methods=['GET', 'POST'])
def questions(act=None):
    """
    最新的
    热门的
    未回答的
    """
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    page = request.args.get('page', 1, type=int)

    if act == 'hottest':
        query = query.order_by(Question.view_num.desc())
    elif act == 'unanswered':
        from sqlalchemy import exists
        query = query.filter(~exists().where(Question.id == Answer.question_id))
        query = query.order_by(Question.create_time.desc())
    else:
        query = query.order_by(Question.create_time.desc())

    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    questions = pagination.items

    # tags
    tags = Tag.query.order_by(Tag.create_time.desc()).limit(15)

    print '>>>'

    return render_template('layout.html', login_form=login_form, register_form=register_form,
                           pagination=pagination, questions=questions, tags=tags, act=act)
