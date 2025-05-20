from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True)
    first_name: str
    last_name: str
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: str | None = None  # type: ignore
    first_name: str | None = None  # type: ignore
    last_name: str | None = None  # type: ignore
    email: str | None = None  # type: ignore


class AppFile(SQLModel, table=True):
    __tablename__ = "files"  # type: ignore

    id: int | None = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    original_name: str
    extension: str
    size: str
    path: str
