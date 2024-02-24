#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        used to add user to table
        """

        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        finds user using kwargs
        """
        if not kwargs:
            raise InvalidRequestError
        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates user with kwargs
        """
        item_attributes = ["id", "email", "hashed_password",
                           "session_id", "reset_token"]
        user = self.find_user_by(id=user_id)
        if not user:
            return None
        for cc in kwargs.keys():
            if cc not in item_attributes:
                raise ValueError
        for column in kwargs.keys():
            if column == item_attributes[0]:
                user.id = kwargs[column]
            if column == item_attributes[1]:
                user.email = kwargs[column]
            if column == item_attributes[2]:
                user.hashed_password = kwargs[column]
            if column == item_attributes[3]:
                user.session_id = kwargs[column]
            if column == item_attributes[4]:
                user.reset_token = kwargs[column]
        self._session.commit()
        return None
