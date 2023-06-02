from __future__ import annotations

from pydantic import BaseModel, validator, AnyUrl, HttpUrl


class _Database(BaseModel):
    url: AnyUrl
    name: str

    @validator('name')
    def name_validator(cls, value: str):
        if all(char.isalpha() or char == "_" for char in value):
            return value
        raise ValueError('the database name can contain only letters and "_"')


class _Redis(BaseModel):
    host: HttpUrl
    port: int

    @validator("port")
    def port_validator(cls, value):
        if 1024 <= value <= 49151:
            return value
        raise ValueError("port can be in the range from 1024 to 49151.")


class _Bot(BaseModel):
    token: str
    log_level: int
    debug: bool

    @validator("log_level")
    def log_level_validator(cls, value):
        if 0 <= value <= 100:
            return value
        raise ValueError("log_level can be in the range from 20 to 100")


class ConfigModel(BaseModel):
    database: _Database
    bot: _Bot
    redis: _Redis
