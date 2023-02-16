#!/usr/bin/env python3
"""
Auth module
"""

import bcrypt
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user into the database
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        except InvalidRequestError:
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        validated login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            bytes = password.encode('utf-8')
            return bcrypt.checkpw(bytes, user.hashed_password)
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """
        Generate UUID for auth
        """
        return str(uuid4())

    def create_session(self, email) -> Union[str, None]:
        """
        create a session
        """
        try:
            user = self._db.find_user_by(email=email)
            id = self._generate_uuid()
            user.session_id = id
            self._db._session.commit()
            return user.session_id
        except Exception:
            return None
