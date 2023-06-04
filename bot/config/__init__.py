import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any

import loguru
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from bot.config.model import ConfigModel

path = os.path.dirname(os.path.abspath(__file__))
variables_path = os.path.abspath(os.path.join(path, '../variables.json'))

with open(variables_path, mode="r", encoding="UTF-8") as file:
    raw_config = json.load(file)


class CustomLogger:
    def __init__(self, debug_enabled: bool = False):
        self.debug_enabled = debug_enabled

        logging_directory = os.path.join(path, '../logs')
        filename = f"log_{datetime.now().strftime('%d.%m.%y')}.txt"

        logging_format = (
            "<magenta>logger</magenta> | "
            "<level>{level: <8}</level> | "
            "<italic><green>{time:DD.MM.YY HH:mm (ss)}</green></italic> | "
            "{name}:{function}:{line} > <level>{message}</level>"
        )

        self.logger = loguru.logger.bind()

        if not os.path.exists(logging_directory):
            os.makedirs(logging_directory)

        loguru.logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "format": logging_format
                }, {
                    "sink": os.path.join(logging_directory, filename),
                    "rotation": "5 MB",
                    "compression": "zip",
                    "format": logging_format
                },
            ]
        )

    def debug(self, message: Any, **kwargs):
        self.logger.debug(message, **kwargs)

    def info(self, message: Any, **kwargs):
        self.logger.info(message, **kwargs)

    def warning(self, message: Any, **kwargs):
        self.logger.warning(message, **kwargs)

    def error(self, message: Any, **kwargs):
        self.logger.error(message, **kwargs)

    def critical(self, message: Any, **kwargs):
        self.logger.critical(message, **kwargs)


config: ConfigModel = ConfigModel(**raw_config)
logger = CustomLogger()

loop = asyncio.get_event_loop()
bot = Bot(token=config.bot.token, parse_mode="html")
storage = RedisStorage2(host=config.redis.host, port=config.redis.port, password=config.redis.password.get_secret_value(), loop=loop, db=5)
dp = Dispatcher(bot, loop=loop, storage=storage)

__all__ = (
    "logger",
    "config",
    "bot",
    "storage",
    "dp",
)
