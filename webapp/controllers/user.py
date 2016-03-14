# coding: utf8
from flask import Blueprint, render_template, url_for, redirect
from ..models.user import User
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('user', __name__)


@bp.route('/<int:id>')
def index(id=None):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user, type='answers')


@bp.route('/<int:id>/<string:type>')
def user_answers(id, type):
    user = User.query.get_or_404(id)
    if type == 'answers':
        pass
    elif type == 'questions':
        pass
    else:
        return redirect(url_for('user.index', id=id))
    return render_template('user.html', user=user, type=type)
