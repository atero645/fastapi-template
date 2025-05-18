from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.internal.repositories.user_repository import UserSQLRepository
from app.internal.services.user_service import UserService


async def pagination_params(limit: int = 20, page: int = 1):
    return {"limit": limit, "page": page}


PaginationParams = Annotated[dict, Depends(pagination_params)]

SessionDep = Annotated[Session, Depends(get_session)]
UserRepoDep = Annotated[UserSQLRepository, Depends()]
UserDep = Annotated[UserService, Depends()]
