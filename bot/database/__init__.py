from bot.config import config, logger

from bot.database.engine import Database
from bot.database.wrapper import DatabaseWrapper

db: DatabaseWrapper = DatabaseWrapper(database_instance=Database(config.database.url, config.database.name))

logger.info("Database connection established.")

__all__ = (
    "db",
)
