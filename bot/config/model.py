from __future__ import annotations

import enum
from typing import Optional

from pydantic import BaseModel, validator, PostgresDsn, RedisDsn, SecretStr, AnyUrl


class LoggingLevel(str, enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class _Database(BaseModel):
    url: Optional[AnyUrl]
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]

    def get_url(self) -> Optional[str]:
        if self.url:
            return self.url
        if all((self.username, self.password, self.host, self.port, self.database)):
            return f"asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        return None

    @validator("port")
    def port_validator(cls, value):
        if 1024 <= value <= 49151:
            return value
        raise ValueError("port can be in the range from 1024 to 49151.")


class _Redis(BaseModel):
    url: Optional[RedisDsn]
    host: Optional[str]
    port: Optional[int]
    password: Optional[SecretStr]

    def get_url(self) -> Optional[str]:
        if self.url:
            return self.url
        if all((self.host, self.port, self.host, self.password)):
            return f"redis://:{self.password}@{self.host}:{self.port}/0"
        return None

    @validator("port")
    def port_validator(cls, value):
        if 1024 <= value <= 49151:
            return value
        raise ValueError("port can be in the range from 1024 to 49151.")


class _Bot(BaseModel):
    token: str
    logging: LoggingLevel
    debug: bool


class ConfigModel(BaseModel):
    database: _Database
    bot: _Bot
    redis: _Redis
