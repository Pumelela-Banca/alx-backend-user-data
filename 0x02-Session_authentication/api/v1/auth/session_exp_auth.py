#!/usr/bin/env python3
"""
Used in session authentication
"""
import os
from datetime import datetime, timedelta
from uuid import uuid4
from flask import request
from api.v1.auth.auth import SessionAuth
from models.user import User



class SessionExpAuth(SessionAuth):
    """
    Extends SessionAuth and adds expiry
    """

    def __init__(self):
        """initialize """
        if not os.getenv("SESSION_DURATION"):
            session_duration: int = 0
        else:
            session_duration: int = int(os.getenv("SESSION_DURATION", '0'))

    def create_session(self, user_id=None):
        """
        overrides super
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user session id
        """
        if not session_id:
            return None
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
