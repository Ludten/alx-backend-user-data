#!/usr/bin/env python3
"""
Module of Session Auth class
"""

from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Union
from uuid import uuid4


class SessionAuth(Auth):
    """
    Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """
        Create a user session
        """
        if user_id is None:
            return None
        if isinstance(user_id, str) is False:
            return None
        s_id = str(uuid4())
        self.user_id_by_session_id[s_id] = user_id
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> Union[
            str, None]:
        """
        Return the user id from the create session
        manager
        """
        if session_id is None:
            return None
        if isinstance(session_id, str) is False:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return current user
        """
        cookid = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookid)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Destroy a session
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
