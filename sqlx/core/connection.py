from __future__ import annotations

from typing import Any, Iterable

from .result import Result
from ..types import Query, Args
from .queries import Insert, Upsert, Select, Update, Delete


class Connection(Select, Insert, Update, Delete):
    def __call__(self, query: str, args: Iterable[Any] = ()) -> Result:
        return Result(
            cnn=self._cnn,
            query=Query().update(query),
            args=Args().update(*args),
        )
