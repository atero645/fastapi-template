from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from app.database import create_db
from app.routers import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
