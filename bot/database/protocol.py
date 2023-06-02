from typing import Protocol, runtime_checkable, Union, Type, List

from pydantic import BaseModel


@runtime_checkable
class DatabaseModel(Protocol):
    async def add(self, data: Union[dict, List[dict]]):
        ...

    async def find(self, data: dict, multiple: bool = False, sort: Union[str, None] = None, model: Type[BaseModel] = None):
        ...

    async def delete(self, data: dict, multiple: bool = False):
        ...

    async def update(self, old_data: dict, new_data: dict, multiple: bool = False, raw: bool = False):
        ...
