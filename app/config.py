from contextvars import ContextVar
from datetime import timedelta
from enum import Enum, auto
import inspect
import os
import tomllib
from typing import Optional
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine
from sqlmodel import create_engine


class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class JWT(BaseModel):
    secret: str
    algorithm: str = "HS256"
    expiration: timedelta = timedelta(minutes=30)
    refresh_expiration: timedelta = timedelta(days=7)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    port: int = 5000
    log_level: LogLevel = LogLevel.INFO
    pg_dsn: Optional[PostgresDsn] = None
    sqlite_dsn: str = "sqlite:///./db.sqlite"
    redis_dsn: str = "redis://localhost:6379/0"
    jwt: JWT
    allowed_origins: list[str] = ["http://localhost", "http://localhost:3000"]
    supabase_url: str = ""
    supabase_key: str = ""

    def build_engine(self) -> Engine:
        db_dsn = self.get_dsn()

        debug = self.log_level == LogLevel.DEBUG

        engine = create_engine(
            db_dsn,
            echo=debug,
        )

        return engine

    def get_dsn(self) -> str:
        pg_dsn = str(self.pg_dsn) if self.pg_dsn else None
        return pg_dsn or self.sqlite_dsn

    def metadata(self) -> dict:
        metadata = {}

        with open("pyproject.toml", "rb") as f:
            project_data = tomllib.load(f)
        metadata.update(project_data["tool"]["poetry"])
        metadata["summary"] = metadata["description"]

        metadata["description"] = "readme"

        return metadata

    def full_path(self, path: str) -> str:
        this_file = os.path.abspath(inspect.stack()[0][1])
        this_file_directory = os.path.dirname(this_file)
        root_directory = os.path.join(this_file_directory, "..")

        return root_directory + path


settings: ContextVar[Settings] = ContextVar(
    "settings",
    default=Settings(),
)
