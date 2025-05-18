from functools import lru_cache
import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, create_engine
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")


@lru_cache
def init_db() -> Engine:
    from app.internal.database.models import User  # noqa: F401

    config = get_settings()
    # logger.info(f"DB INIT {config}")

    sqlite_url = f"sqlite:///{config.sqlite_db_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args, pool_size=30)

    SQLModel.metadata.create_all(engine)

    return engine


def get_session(engine: Annotated[Engine, Depends(init_db)]):
    with Session(engine) as session:
        yield session
