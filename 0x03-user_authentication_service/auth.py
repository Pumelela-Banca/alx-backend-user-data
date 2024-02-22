#!/usr/bin/env python3
"""
authentication hashing of password
"""
import bcrypt


def _hash_password(password: str) -> str:
    """
    uses bcrypt to encrypt password
    """
    new_p = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(new_p, salt)
