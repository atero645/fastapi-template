from .files_router import router as FilesRouter
from .users_router import router as UsersRouter

routers = [
    UsersRouter,
    FilesRouter,
]
