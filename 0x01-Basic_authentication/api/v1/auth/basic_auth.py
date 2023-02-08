#!/usr/bin/env python3
"""
Module of Basic Auth class
"""

import base64
from typing import List, Tuple, TypeVar, Union

from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Authentication class
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> Union[str, None]:
        """
        get base64 auth from header
        """
        if authorization_header is None:
            return None
        if isinstance(authorization_header, str) is False:
            return None
        if authorization_header.startswith('Basic '):
            basic = authorization_header.split()
            return basic[1]
        return None

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> Union[str, None]:
        """
        decode base64 auth
        """
        if base64_authorization_header is None:
            return None
        if isinstance(base64_authorization_header, str) is False:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        Extract user credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if isinstance(decoded_base64_authorization_header, str) is False:
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            basic = decoded_base64_authorization_header.split(':', 1)
            return (basic[0], basic[1])
        return (None, None)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> Union[TypeVar('User'), None]:
        """
        Create a user object
        """
        if user_email is None or isinstance(user_email, str) is False:
            return None
        if user_pwd is None or isinstance(user_pwd, str) is False:
            return None
        User.load_from_file()
        if User.count() > 0:
            users = User.search({'email': user_email})
            if users != []:
                for usr in users:
                    if isinstance(usr, User):
                        if usr.is_valid_password(user_pwd):
                            return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        return current user
        """
        header = self.authorization_header(request)
        b64 = self.extract_base64_authorization_header(header)
        db64 = self.decode_base64_authorization_header(b64)
        cred = self.extract_user_credentials(db64)
        usr = self.user_object_from_credentials(*cred)
        return usr
