#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, request, current_app
from ..forms.user import LoginForm, RegisterForm
from ..models.question import Question, Tag

bp = Blueprint('tag', __name__)


@bp.route('/<int:tag_id>')
def index(tag_id=None):

    page = request.args.get('page', 1, type=int)
    query = Question.query.filter(Question.tags.any(Tag.id == tag_id))
    pagination = query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                error_out=False)
    questions = pagination.items

    return render_template('tag.html', pagination=pagination, questions=questions,
                           page=page, tag_id=tag_id)
