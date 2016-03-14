# coding: utf8
from flask import Blueprint, render_template, url_for, redirect, current_app, request
from ..models.user import User
from ..models.question import Question, Answer
from .. import cache
from ..forms.user import LoginForm, RegisterForm

bp = Blueprint('user', __name__)


@bp.route('/<int:id>')
@bp.route('/<int:id>/<string:type>')
def index(id, type='questions'):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    if type == 'answers':
        query = Answer.query.filter(Answer.author_id == id).order_by(Answer.create_time.desc())
    elif type == 'questions':
        query = Question.query.filter(Question.author_id == id).order_by(Question.create_time.desc())
    else:
        return redirect(url_for('.index', id=id))

    pagination = query.paginate(page, per_page=5,
                                error_out=False)
    qa = pagination.items
    return render_template('user.html', user=user, type=type,
                           page=page, pagination=pagination, qa=qa)
