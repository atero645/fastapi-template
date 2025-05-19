from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "FastAPI template"
    admin_email: str = ""
    app_secret: str = "secret"
    db_host: str = ""
    db_port: int = 3306
    db_user: str = ""
    db_pass: str = ""
    db_database: str = "postgres"
    sqlite_db_name: str = "local.db"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return AppSettings()
