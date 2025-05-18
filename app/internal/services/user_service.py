from fastapi import HTTPException
from app.internal.database.models import User, UserUpdate
from app.internal.repositories.user_repository import UserRepository


class UserService:
    repository: UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, id: int) -> User | None:
        user = self.repository.get_user_by_id(id)
        return user

    def get_users(self, limit=10, page=1) -> list[User]:
        offset = limit * (page - 1)
        users_db = self.repository.get_users(limit, offset)
        return list(users_db)

    def create_user(self, user: User):
        user = self.repository.create_user(user)
        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user_db = self.repository.get_user_by_id(user_id)
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found!")

        update_data = user_data.model_dump(exclude_unset=True)
        user_db.sqlmodel_update(update_data)

        user_db = self.repository.update_user(user_db)

        return user_db
