#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

from flask import Blueprint, render_template, redirect, url_for, request, current_app
from ..models import User, Question, Answer, Tag
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('question.index'))


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
