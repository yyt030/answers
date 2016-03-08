# coding: utf8
from flask import Blueprint, render_template
from ..models.user import User
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('user', __name__)


@bp.route('/<int:id>')
def index(id=None):
    login_form = LoginForm()
    register_form = RegisterForm()
    user = User.query.get_or_404(id)
    print '>>>', user
    return render_template('user.html', login_form=login_form, register_form=register_form)
