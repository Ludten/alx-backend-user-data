#!/usr/bin/env python3
"""
flask app module
"""


from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
