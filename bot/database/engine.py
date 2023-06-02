from typing import Union, Type, List

import motor.motor_asyncio
from pydantic import AnyUrl, BaseModel


class Database:
    def __init__(self, connection_url: AnyUrl, database_name: str, collection_name: str = None):
        self._database = motor.motor_asyncio.AsyncIOMotorClient(connection_url)[database_name]
        self._collection = collection_name

    async def add(self, data: Union[dict, List[dict]]):
        if isinstance(data, list):
            return (await self._database[self._collection].insert_many(data)).inserted_ids
        else:
            return (await self._database[self._collection].insert_one(data)).inserted_id

    async def find(self, data: dict, multiple: bool = False, sort: Union[str, None] = None, model: Type[BaseModel] = None):
        if multiple is True:
            cursor = self._database[self._collection].find(data, {"addresses": {"$slice": [0, 1]}, "_id": 0})

            if sort is not None:
                cursor = cursor.sort(sort)

            documents = await cursor.to_list(int(1e10))
            return [model(**document) for document in documents] if model else documents

        else:
            document = await self._database[self._collection].find_one(data, {"addresses": {"$slice": [0, 1]}, "_id": 0})
            return model(**document) if model and document else document

    async def delete(self, data: dict, multiple: bool = False):
        if multiple is True:
            return (await self._database[self._collection].delete_many(data)).deleted_count
        else:
            return (await self._database[self._collection].delete_one(data)).deleted_count

    async def update(self, old_data: dict, new_data: dict, multiple: bool = False, raw: bool = False):
        if not raw:
            if multiple is True:
                return (await self._database[self._collection].update_many(
                    old_data, {"$set": new_data}
                )).modified_count
            else:
                return (await self._database[self._collection].update_one(
                    old_data, {"$set": new_data}
                )).modified_count
        else:
            return (await self._database[self._collection].update_one(
                old_data, new_data
            )).modified_count
