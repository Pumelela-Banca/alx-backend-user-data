#!/usr/bin/env python3
"""
Used in session authentication
"""
import re
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    Implements session Auth
    """
    pass
