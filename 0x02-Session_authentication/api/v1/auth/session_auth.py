#!/usr/bin/env python3
"""
Used in session authentication
"""
from uuid import uuid4
from flask import request
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    Implements session Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates session ID for user id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user based on Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        (overload) that returns a User instance
        based on a cookie value
        """
        cookie_id = self.session_cookie(request)
        if not cookie_id:
            return None
        user_for_session = self.user_id_for_session_id(cookie_id)
        if not user_for_session:
            return None
        return User.get(user_for_session)

    def destroy_session(self, request=None):
        """
        deletes the user session / logout
        """
        if not request:
            return False
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if session_id is None or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
