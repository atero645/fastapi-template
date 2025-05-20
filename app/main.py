from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from app.internal.middlewares.file_middleware import LimitUploadSizeMiddleware
from app.database import init_db
from app.routers import users_router, files_router


logger = logging.getLogger("uvicorn.error")


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db()
        yield

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(LimitUploadSizeMiddleware)

    app.include_router(users_router.router)
    app.include_router(files_router.router)

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
