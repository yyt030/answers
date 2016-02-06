#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from ..forms.user import LoginForm, RegisterForm
from ..models import User, Question, Answer, Tag

bp = Blueprint('question', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    page = request.args.get('page', 1, type=int)

    pagination = query.order_by(Question.create_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    questions = pagination.items

    return render_template('layout.html',
                           login_form=login_form,
                           register_form=register_form,
                           questions=questions, pagination=pagination)


@bp.route('/hottest')
def hottest():
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    page = request.args.get('page', 1, type=int)

    pagination = query.order_by(Question.create_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    questions = pagination.items

    return render_template('layout.html',
                           login_form=login_form,
                           register_form=register_form,
                           questions=questions, pagination=pagination, act='hottest')


@bp.route('/unanswered')
def unanswered():
    login_form = LoginForm()
    register_form = RegisterForm()
    query = Question.query

    page = request.args.get('page', 1, type=int)

    pagination = query.order_by(Question.create_time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
    questions = pagination.items

    return render_template('layout.html',
                           login_form=login_form,
                           register_form=register_form,
                           questions=questions, pagination=pagination, act='unanswered')
