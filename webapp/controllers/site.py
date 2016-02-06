#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request
from ..models import User, Question, Answer, Tag
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    register_form = RegisterForm()
    questions = Question.query.all()
    return render_template('layout.html',
                           login_form=login_form,
                           register_form=register_form,
                           questions=questions)


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
