from aiogram import Dispatcher
from aiogram.utils import executor

from bot.config import logger, dp


async def startup(dp: Dispatcher) -> None:
    logger.info("bot started")


async def shutdown(dp: Dispatcher) -> None:
    logger.info("bot finished")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
