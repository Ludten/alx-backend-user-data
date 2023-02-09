#!/usr/bin/env python3
"""
Module of Session DB Auth class
"""

from typing import List, Union

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Session DB Authentication class
    """

    def create_session(self, user_id: str = None) -> str:
        """
        Create a user session
        """
        s_id = super().create_session(user_id)
        userss = UserSession()
        userss.user_id = user_id
        userss.session_id = s_id
        userss.save()
        return userss.session_id

    def user_id_for_session_id(self, session_id: str = None) -> Union[
            str, None]:
        """
        Return the user id from the create session
        manager
        """
        UserSession.load_from_file()
        if UserSession.count() > 0:
            users: List[UserSession] = UserSession.search(
                {"session_id": session_id})
            if users != []:
                return users[0].user_id
        return None

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
        users: List[UserSession] = UserSession.search(
            {"session_id": cookie})
        if users != []:
            users[0].remove()
            return True
        return False
