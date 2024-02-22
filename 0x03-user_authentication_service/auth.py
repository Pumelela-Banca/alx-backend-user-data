#!/usr/bin/env python3
"""
authentication hashing of password, class
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> str:
    """
    uses bcrypt to encrypt password
    """
    new_p = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(new_p, salt)


def _generate_uuid() -> str:
    """
    generates UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers user to  db
        """
        try:
            new_user = self._db.find_user_by(email=email)
        except (NoResultFound, InvalidRequestError):
            new_pass = _hash_password(password)
            return self._db.add_user(email, new_pass)
        raise ValueError(f"<user's {email}> already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
        checks password validity
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                return False
        except (InvalidRequestError, NoResultFound):
            return False
        if bcrypt.checkpw(password.encode('utf-8'),
                          user.hashed_password):
            return True
        return False


