from fastapi import APIRouter, HTTPException
from app.dependencies import UserRepoDep, PaginationParams
from app.internal.database.models import User, UserCreate, UserPublic, UserUpdate
from app.internal.services.user_service import UserService

router = APIRouter(tags=["users"])


@router.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, user_repository: UserRepoDep):
    user_service = UserService(user_repository)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/", response_model=list[UserPublic])
def read_users(
    pagination: PaginationParams,
    user_repository: UserRepoDep,
):
    user_service = UserService(user_repository)
    data = user_service.get_users(**pagination)
    return data


@router.post("/users/", response_model=UserPublic, status_code=201)
def create_user(
    user: UserCreate,
    user_repository: UserRepoDep,
):
    user_service = UserService(user_repository)
    db_user = User.model_validate(user)
    data = user_service.create_user(db_user)
    return data


@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdate,
    user_repository: UserRepoDep,
):
    user_service = UserService(user_repository)
    data = user_service.update_user(user_id, user)
    return data
