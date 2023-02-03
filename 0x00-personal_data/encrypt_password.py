#!/usr/bin/env python3
"""
Encrypting passwords module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash password
    """
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    check if a password match
    """
    bytes = password.encode('utf-8')
    return bcrypt.checkpw(bytes, hashed_password)
