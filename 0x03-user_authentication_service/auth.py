#!/usr/bin/env python3
"""
authentication hashing of password, class
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4

from db import DB
from user import User


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
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """
        creates session id and stores it in db
        """
        try:
            user = self._db.find_user_by(email)
        except (InvalidRequestError, NoResultFound):
            return None
        self._db.update_user(user.id, session_id=_generate_uuid())
        return user.session_id
