from tortoise import Tortoise

from bot.config import config, logger


async def init():
    await Tortoise.init(
        db_url=config.database.get_url(),
        modules={'models': ['bot.database.models']}
    )

    await Tortoise.generate_schemas()

    logger.info("Database connection established")


async def close_connections():
    await Tortoise.close_connections()

    logger.info("Database connections terminated")
