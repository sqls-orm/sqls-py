from abc import abstractmethod
from typing import Self

from pydantic import BaseModel

from .column import Column


class Schema(BaseModel):
    @property
    @abstractmethod
    def __table__(self) -> str:
        ...

    @classmethod
    def model(cls) -> Self:
        return type(f'{cls.__name__}SQLX', (), {name: Column(name) for name in cls.__annotations__.keys()})
