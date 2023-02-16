#!/usr/bin/env python3
"""
flask app module
"""


from auth import Auth
from flask import Flask, jsonify, request, abort


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    GET /
    Return:
      - Bienvenue
    """
    return jsonify({"message": "Bienvenue"})


AUTH = Auth()


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    POST /users
    JSON body:
      - email
      - password
    Return:
      - creation message on success
      - error message on failure
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(user.email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /sessions
    JSON body:
      - email
      - password
    Return:
      - creation message on success
      - error message on failure
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == "":
        abort(401)
    if password is None or password == "":
        abort(401)
    if AUTH.valid_login(email, password):
        s_id = AUTH.create_session(email)
        out = jsonify({"email": "{}".format(email),
                       "message": "logged in"})
        out.set_cookie("session_id", s_id)
        return out
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /sessions
    Return:
      - delete session on success
      - abort(403) on failure
    """
    if request is None:
        abort(403)
    s_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(s_id)
    if user:
        AUTH.destroy_session(user.id)
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    POST /profile
    Return:
      - profile object on success
      - error message on failure
    """
    if request is None:
        abort(403)
    s_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(s_id)
    if user:
        return jsonify({"email": "{}".format(user.email)})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    POST /reset_password
    JSON body:
      - email
    Return:
      - reset token on success
      - abort(403) on failure
    """
    email = request.form.get('email')
    if email is None or email == "":
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": "{}".format(email),
                       "reset_token": "{}".format(token)})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    PUT /reset_password
    JSON body:
      - email
    Return:
      - update user password on success
      - abort(403) on failure
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('new_password')
    if email is None or email == "":
        abort(403)
    if reset_token is None or reset_token == "":
        abort(403)
    if password is None or password == "":
        abort(403)
    try:
        AUTH.update_password(reset_token, password)
        return jsonify({"email": "{}".format(email),
                       "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
