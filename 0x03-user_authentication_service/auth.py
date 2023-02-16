#!/usr/bin/env python3
"""
Auth module
"""

from uuid import uuid4
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    bytes = password.encode()
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    """
    Generate UUID for auth
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user into the database
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        validated login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes = password.encode()
            return bcrypt.checkpw(bytes, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email) -> Union[str, None]:
        """
        create a session
        """
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            user.session_id = id
            self._db._session.commit()
            return user.session_id
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get a user from the database
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session in the db
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            self._db._session.commit()
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            t_id = str(uuid4())
            user.reset_token = t_id
            self._db._session.commit()
            return t_id
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            self._db._session.commit()
        except Exception:
            raise ValueError
