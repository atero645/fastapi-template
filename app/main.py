from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI
from app.database import init_db
from app.routers import users_router


logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router.router)


@app.get("/")
def read_root():
    return "API Started!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
