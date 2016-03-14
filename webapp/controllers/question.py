#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask.ext.login import current_user, login_required
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question, Answer, Tag

from .. import db, cache

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
        answer = Answer(question_id=question_id, author_id=current_user.id,
                        title=answer_data[1:100], body_html=answer_data)
        db.session.add(answer)
        db.session.commit()
    return render_template('question.html', question=question)
