from abc import ABC, abstractmethod
from sqlmodel import Session, select
from typing import Annotated
from fastapi import Depends
from app.database import get_session
from app.internal.database.models import User


class UserRepository(ABC):
    # session: Session

    # @abstractmethod
    # def __init__(self, session: Annotated[Session, Depends(get_session)]):
    #     pass

    @abstractmethod
    def get_user_by_id(self, id: int) -> User | None:
        pass

    @abstractmethod
    def get_users(self, limit: int, offset: int) -> list[User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass


class UserSQLRepository(UserRepository):
    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get_user_by_id(self, id: int) -> User | None:
        user = self.session.get(User, id)
        return user

    def get_users(self, limit: int, offset: int) -> list[User]:
        users_db = self.session.exec(select(User).offset(offset).limit(limit)).all()
        return list(users_db)

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
