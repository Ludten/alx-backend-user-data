#!/usr/bin/env python3
"""
Main module
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    test user register
    """
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    userauth = requests.post(url=url, data=data)
    assert userauth.status_code == 200
    assert userauth.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test wrong password
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    userauth = requests.post(url=url, data=data)
    assert userauth.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    test login
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    userauth = requests.post(url=url, data=data)
    assert userauth.json() == {"email": email, "message": "logged in"}
    assert userauth.status_code == 200
    assert 'session_id' in userauth.cookies.keys()
    return userauth.cookies["session_id"]


def profile_unlogged() -> None:
    """
    test profile while not logged in
    """
    url = 'http://localhost:5000/profile'
    userauth = requests.get(url=url)
    assert userauth.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    test profile check
    """
    url = 'http://localhost:5000/profile'
    cookie = {'session_id': session_id}
    userauth = requests.get(url=url, cookies=cookie)
    assert userauth.status_code == 200
    assert "email" in userauth.json()


def log_out(session_id: str) -> None:
    """
    test logout
    """
    url = 'http://localhost:5000/sessions'
    cookie = {'session_id': session_id}
    userauth = requests.delete(url=url, cookies=cookie, allow_redirects=False)
    assert userauth.status_code == 302


def reset_password_token(email: str) -> str:
    """
    test password reset token
    """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    userauth = requests.post(url=url, data=data)
    assert userauth.status_code == 200
    assert "reset_token" in userauth.json()
    return userauth.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test password update
    """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    userauth = requests.put(url=url, data=data)
    assert userauth.status_code == 200
    assert userauth.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
