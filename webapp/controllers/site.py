#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import re
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask.ext.login import current_user, login_required
from sqlalchemy import func
from .. import db
from ..forms.question import QuestionForm
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question, Tag, Answer
from ..models.user import Permission

bp = Blueprint('site', __name__)


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@bp.route('/')
def index():
    return redirect(url_for('.questions', act='newest'))


@bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')

    return redirect(url_for('.index', q=q))


@bp.route('/login', methods=['GET'])
def login():
    return redirect(url_for('user_api.login'))


@bp.route('/tags', methods=['GET'])
def tags():
    return redirect(url_for('.index'))


@bp.route('/tour')
def tour():
    return redirect(url_for('.index'))


@bp.route('/questions')
@bp.route('/questions/<string:act>')
def questions(act='newest'):
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
    elif act == 'newest':
        query = query.order_by(Question.create_time.desc())

    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    questions = pagination.items

    # 热议标签
    tags = db.session.query(Tag).join(Tag, Question.tags) \
        .group_by(Tag.name).order_by(Question.view_num.desc()).limit(10)
    # 最近热门
    last_hot_questions = db.session.query(Question).join(Answer) \
        .group_by(Question.title).order_by(Answer.create_time.desc(),
                                           func.count(Answer.id).desc()).limit(10)

    return render_template('index.html', login_form=login_form, register_form=register_form,
                           pagination=pagination, questions=questions,
                           tags=tags, act=act, page=page, last_hot_questions=last_hot_questions)


@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    login_form = LoginForm()
    register_form = RegisterForm()
    question_form = QuestionForm()
    if request.method == 'POST' and question_form.validate_on_submit():
        question = Question(title=question_form.title.data, body=request.form.get('body'), author_id=current_user.id)
        tag_list = re.split(r'[,;]', question_form.tags.data)
        for t in tag_list:
            t = t.replace(r' ', '')
            tag = Tag.query.filter(Tag.name == t).first()
            if not tag:
                tag = Tag(name=t)
            question.tags.append(tag)

        db.session.add(question)
        db.session.commit()
        return redirect(url_for('site.index'))

    return render_template('ask.html', login_form=login_form, register_form=register_form,
                           question_form=question_form)
