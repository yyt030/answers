# coding: utf8
from flask import Blueprint, render_template, jsonify
from .. import db
from ..forms.user import LoginForm, RegisterForm
from ..models.user import User

bp = Blueprint('user', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')
