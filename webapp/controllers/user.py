# coding: utf8
from flask import Blueprint, render_template
from ..models.user import User
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('user', __name__)


@bp.route('/<int:id>')
def index(id=None):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)
