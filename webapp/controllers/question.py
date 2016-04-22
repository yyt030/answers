#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import datetime
import random

import os
import re
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask.ext.login import current_user, login_required
from .. import db
from ..models.question import Question, Answer, Tag

bp = Blueprint('question', __name__)


@bp.route('/')
@bp.route('/<int:question_id>')
# @cache.cached()
def questions(question_id=None):
    """问题详情"""
    if not question_id:
        return redirect(url_for('site.index'))
    question = Question.query.get_or_404(question_id)

    # 问题下回答的分页
    page = request.args.get('page', 1, type=int)
    answers_query = Answer.query.filter(Answer.question_id == question_id).order_by(Answer.create_time.desc())

    pagination = answers_query.paginate(page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
                                        error_out=False)
    answers = pagination.items

    # 增加问题的浏览量
    question.view_num += 1
    db.session.add(question)
    db.session.commit()

    # 查询相似问题 similar
    similar_question = Question.query.limit(10)
    sim_id_list = []
    for i in question.tags.all():
        sim_id_list.append(i.id)
    if sim_id_list:
        similar_question = Question.query.filter(
            Question.tags.any(Tag.id.in_(sim_id_list)), Question.id != question.id).limit(10)

    return render_template('question.html', question=question, similar_question=similar_question,
                           answers=answers, pagination=pagination, page=page)


@bp.route('/<int:question_id>/answers/add', methods=['GET', 'POST'])
@login_required
def answers_add(question_id):
    """问题详情"""
    question = Question.query.get_or_404(question_id)
    answer_data = request.form.get('answer_data')

    if answer_data:
        save_image_dir = r'/static/images/qa_images'
        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        reg = re.compile(r'<img src=.*?>')
        image_list = reg.findall(answer_data)
        if image_list:
            filenames = ['{}-{:03}.png'.format(current_time, random.randint(0, 1000))
                         for i in xrange(len(image_list))]
            # 保存图像
            for i, filename in enumerate(filenames):
                image_base64_data = ((image_list[i].split('"'))[1].split(','))[1]
                with open(os.path.join(current_app.config['SAVE_IMAGE_DEST'], filename), 'wb') as f:
                    f.write(image_base64_data.decode('base64'))

            # 将image data 替换为文件路径
            answer_data = reg.sub('<img src="{}/{}">'.format(save_image_dir, *filenames), answer_data)

        answer = Answer(question_id=question_id, author_id=current_user.id,
                        title=answer_data[1:100], body_html=answer_data)
        db.session.add(answer)
        db.session.commit()
    return render_template('question.html', question=question)
