#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Tuple

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, *details: Tuple[str, ...]) -> User :
        """
        used to add user to table
        """
        if len(details) < 2:
            return None
        if not self._session:
            new_sesh: sessionmaker = self._session()
        else:
            new_sesh: sessionmaker = self.__session

        user = User(email=details[0],
                    hashed_password=details[1])
        new_sesh.add(user)
        new_sesh.commit()
        return user
