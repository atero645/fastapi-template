from functools import lru_cache
import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy import Engine, URL
from sqlmodel import SQLModel, Session, create_engine
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")


@lru_cache
def init_db() -> Engine:
    from app.internal.database.models import User, AppFile  # noqa: F401

    config = get_settings()

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=config.db_user,
        password=config.db_pass,
        host=config.db_host,
        port=config.db_port,
        database=config.db_database,
    )

    try:
        engine = create_engine(db_url, pool_size=30, pool_pre_ping=True)
        SQLModel.metadata.create_all(engine)
    except Exception as error:
        logger.error("ERROR CONNECT TO DB!")
        raise error

    return engine


def get_session(engine: Annotated[Engine, Depends(init_db)]):
    with Session(engine) as session:
        yield session
