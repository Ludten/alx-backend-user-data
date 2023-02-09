#!/usr/bin/env python3
"""
Module of Session Expiration Auth class
"""

from datetime import datetime, timedelta
from typing import Union
from api.v1.auth.session_auth import SessionAuth
import os


class SessionExpAuth(SessionAuth):
    """
    Session Expiration Authentication class
    """

    def __init__(self):
        super().__init__()
        if int(os.environ.get('SESSION_DURATION')):
            self.session_duration = int(os.environ.get('SESSION_DURATION'))
        else:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """
        Create a user session
        """
        sess = super().create_session(user_id)
        if sess is None:
            return None
        if isinstance(sess, str) is False:
            return None
        self.user_id_by_session_id[sess] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return sess

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
        if session_id not in self.user_id_by_session_id:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return sess_dict.get("user_id")
        if "created_at" not in sess_dict:
            return None
        if timedelta(seconds=self.session_duration) + sess_dict.get(
                "created_at") < datetime.now():
            return None
        return sess_dict.get("user_id")
