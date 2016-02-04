from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..models import User

bp = Blueprint('user', __name__)


@bp.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return render_template('index.html')


@bp.route('/login', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('password')
    remember = request.form.get('remember')
    print '>>>', mail, password, remember
    return jsonify({
        'status': 0,
        'data': "https://segmentfault.com/",
        'message': 'ok'
    })


@bp.route('/register', methods=['POST', 'GET'])
def register():
    pass
    return render_template('index.html')
