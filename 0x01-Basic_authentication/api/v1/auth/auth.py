#!/usr/bin/env python3
"""
Module of Auth class
"""

from typing import List, TypeVar, Union
from flask import request


class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check auth status
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for paths in excluded_paths:
            if paths.endswith('*'):
                if paths[:-1] in path:
                    return False
            else:
                if path in paths or path + '/' in paths:
                    return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """
        Set authorization header
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        set current user
        """
        return None
