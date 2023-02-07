#!/usr/bin/env python3
"""
Module of Auth class
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check auth status
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Set authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        set current user
        """
        return None
