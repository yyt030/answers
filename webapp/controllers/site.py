#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import datetime
import random

import os
import re
from flask import Blueprint, render_template, redirect, url_for, request, current_app, send_from_directory, abort
from flask.ext.login import current_user, login_required
from sqlalchemy import func
from .. import db, cache
from ..forms.question import QuestionForm
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


@bp.route('/download')
@bp.route('/download/<path:filename>')
def download(filename=None):
    if not filename:
        return render_template('download.html')
    return send_from_directory(directory=current_app.config['DOWNLOAD_DEFAULT_DEST'],
                               filename=filename)


@bp.route('/search')
def search():
    query = None;
    search = request.args.get('q', '')
    if not search:
        return redirect(url_for('.index'))
    else:
        query = Question.query.whoosh_search(search, or_=True,
                                             limit=current_app.config['FLASKY_POSTS_PER_PAGE']).order_by(
            Question.create_time.desc())
    count = len(query.all())

    questions = query
    return render_template('search.html', questions=questions, count=count)


@bp.route('/login', methods=['GET'])
def login():
    return redirect(url_for('user_api.login'))


@bp.route('/tags', methods=['GET'])
@cache.cached()
def tags():
    tags = Tag.query.all()
    tag_categorys = db.session.query(func.distinct(Tag.category)).all()
    return render_template('tags.html', tags=tags, tag_categorys=tag_categorys)


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
    else:
        return abort(404)

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

    return render_template('index.html', pagination=pagination, questions=questions,
                           tags=tags, act=act, page=page, last_hot_questions=last_hot_questions)


@bp.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    question_form = QuestionForm()
    if request.method == 'POST' and question_form.validate_on_submit():
        question_data = request.form.get('body')
        if question_data:
            save_image_dir = r'/static/images/qa_images'
            current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            reg = re.compile(r'<img src="data:image/jpeg;base64.*?>')
            image_list = reg.findall(question_data)
            if image_list:
                filenames = ['%s-%03d.png' % (current_time, random.randint(0, 1000))
                             for i in xrange(len(image_list))]
                # 保存图像
                if not os.path.exists(current_app.config['SAVE_IMAGE_DEST']):
                    os.mkdir(current_app.config['SAVE_IMAGE_DEST'])

                for i, filename in enumerate(filenames):
                    image_base64_data = ((image_list[i].split('"'))[1].split(','))[1]
                    with open(os.path.join(current_app.config['SAVE_IMAGE_DEST'], filename), 'wb') as f:
                        f.write(image_base64_data.decode('base64'))
                    # 将image data 替换为文件路径
                    question_data = reg.sub('<img src="%s/%s">' % (save_image_dir, filename), question_data)

        question = Question(title=question_form.title.data, body_html=question_data,
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

    return render_template('ask.html', question_form=question_form)
