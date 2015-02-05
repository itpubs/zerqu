# coding: utf-8

from flask import Blueprint, request
from flask import jsonify
from werkzeug.datastructures import MultiDict
from .base import require_oauth, require_confidential
from .base import cursor_query, int_or_raise
from ..models import current_user, User
from ..forms import RegisterForm

bp = Blueprint('api_users', __name__)


@bp.route('/users', methods=['POST'])
@require_confidential
def create_user():
    form = RegisterForm(MultiDict(request.json), csrf_enabled=False)
    if not form.validate():
        return jsonify(
            status='error',
            error_code='error_form',
            error_form=form.errors,
        ), 400
    user = form.create_user()
    return jsonify(status='ok', data=user), 201


@bp.route('/users')
@require_oauth(login=False)
def list_users():
    count = int_or_raise('count', 20, 100)
    q = cursor_query(User)
    data = q.order_by(User.id.desc()).limit(count).all()
    return jsonify(status='ok', data=data)


@bp.route('/user')
@require_oauth(login=True)
def view_current_user():
    return jsonify(status='ok', data=current_user)


@bp.route('/user', methods=['PATCH'])
@require_oauth(True, 'user:write')
def update_current_user():
    return 'todo'


@bp.route('/users/<username>')
@require_oauth(login=False)
def view_user(username):
    return 'todo'
