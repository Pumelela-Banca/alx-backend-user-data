#!/usr/bin/env python3
"""
Used in session authentication
"""
from uuid import uuid4
from flask import request
from api.v1.auth.auth import Auth


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
