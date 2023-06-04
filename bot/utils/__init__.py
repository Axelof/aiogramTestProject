import asyncio
from platform import platform

from bot.config import logger

if platform == "linux" or platform == "linux2":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    if logger.debug_enabled:
        logger.debug("uvloop \"EventLoopPolicy\" configured")

loop = asyncio.get_event_loop()

__all__ = (
    loop,
)
