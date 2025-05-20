from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from app.internal.middlewares import middlewares
from app.database import init_db
from app.routers import routers


logger = logging.getLogger("uvicorn.error")


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db()
        yield

    app = FastAPI(lifespan=lifespan)

    for middleware in middlewares:
        app.add_middleware(middleware)

    for router in routers:
        app.include_router(router)

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
