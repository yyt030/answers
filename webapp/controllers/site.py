#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import re
from flask import Blueprint, render_template, redirect, url_for, request, current_app, send_from_directory
from flask.ext.login import current_user, login_required
from sqlalchemy import func
from .. import db, cache
from ..forms.question import QuestionForm
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question, Tag, Answer
from ..models.user import Permission

bp = Blueprint('site', __name__)


@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@bp.route('/')
@bp.route('/sites')
def index():
    return redirect(url_for('.questions', act='newest'))


@bp.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(directory=current_app.config['DOWNLOAD_DEFAULT_DEST'],
                               filename=filename)


@bp.route('/search')
def search():
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    search = request.args.get('q', '')

    if not search:
        return redirect(url_for('.index'))
    else:
        query = query.filter((Question.title.contains(search) | (Question.body.contains(search))))

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    count = query.count()
    questions = pagination.items

    return render_template('search.html', login_form=login_form, register_form=register_form,
                           pagination=pagination, questions=questions, page=page, count=count)


@bp.route('/login', methods=['GET'])
def login():
    return redirect(url_for('user_api.login'))


@bp.route('/tags', methods=['GET'])
@cache.cached()
def tags():
    login_form = LoginForm()
    register_form = RegisterForm()

    tags = Tag.query.all()
    tag_categorys = db.session.query(func.distinct(Tag.category)).all()
    return render_template('tags.html', login_form=login_form, register_form=register_form,
                           tags=tags, tag_categorys=tag_categorys)


@bp.route('/tour')
def tour():
    return redirect(url_for('.index'))


@bp.route('/vote', methods=['POST'])
def vote():
    data_type = request.form.get('data_type', '')
    data_id = request.form.get('data_id', '')
    data_number = request.form.get('data_number', 0, type=int)
    if data_type == 'question':
        question = Question.query.get_or_404(data_id)
        if question:
            question.vote_num += data_number
            db.session.add(question)
            db.session.commit()
    elif data_type == 'answer':
        answer = Answer.query.get_or_404(data_id)
        if answer:
            answer.vote_num += data_number
            db.session.add(answer)
            db.session.commit()
    return ''


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
        query = query.order_by(Question.vote_num.desc(), Question.view_num.desc())
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
        question = Question(title=question_form.title.data, body_html=request.form.get('body'),
                            author_id=current_user.id)
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
