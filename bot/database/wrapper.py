from src.database.protocol import DatabaseModel


class DatabaseWrapper:
    def __init__(self, database_instance: DatabaseModel):
        self._database_instance: DatabaseModel = database_instance

    def by(self, collection: str) -> DatabaseModel:
        self._database_instance._collection = collection
        return self._database_instance
