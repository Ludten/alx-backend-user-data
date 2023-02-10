#!/usr/bin/env python3
"""
Route module for the API
"""


from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.environ.get('AUTH_TYPE'):
    if os.environ.get('AUTH_TYPE') == 'basic_auth':
        auth = BasicAuth()
    elif os.environ.get('AUTH_TYPE') == 'session_auth':
        auth = SessionAuth()
    elif os.environ.get('AUTH_TYPE') == 'session_exp_auth':
        auth = SessionExpAuth()
    elif os.environ.get('AUTH_TYPE') == 'session_db_auth':
        auth = SessionExpAuth()
    else:
        auth = Auth()


@app.before_request
def before_request() -> None:
    """
    Valid authentication
    """
    pathlist = ['/api/v1/status/', '/api/v1/unauthorized/',
                '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if auth is not None:
        if auth.require_auth(request.path, pathlist) is True:
            if auth.authorization_header(
                    request) is None and auth.session_cookie(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)
            request.current_user = auth.current_user(request)


@app.errorhandler(401)
def not_found(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_found(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)