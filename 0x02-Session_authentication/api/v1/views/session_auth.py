#!/usr/bin/env python3
""" Module of Session authentication views
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os
from typing import List


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def create_session() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - Session authentication object JSON represented
      - 400 if can't create the new Session
    """
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        return jsonify({'error': "email missing"}), 400
    if password is None or password == "":
        return jsonify({'error': "password missing"}), 400
    users: List[User] = User.search({'email': email})
    if users != []:
        for usr in users:
            if usr.is_valid_password(password):
                s_id = auth.create_session(usr.id)
                out = jsonify(usr.to_json())
                out.set_cookie(os.environ.get('SESSION_NAME'), s_id)
                return out
        return jsonify({'error': "wrong password"}), 401
    return jsonify({'error': "no user found for this email"}), 404


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON is the Session has been correctly deleted
      - 404 if the Session ID doesn't exist
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
