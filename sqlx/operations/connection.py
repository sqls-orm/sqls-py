from __future__ import annotations

from typing import Any, Iterable, Union

import aiomysql

from .delete import Delete
from .insert import Insert
from .result import Result
from .select import Select
from .update import Update
from ..types import Schema, Column, Query, Args


class Connection:
    def __init__(self, cnn: aiomysql.Connection):
        self._cnn: aiomysql.Connection = cnn

    def select[S: Schema](self, *columns: Iterable[Union[Column, str]], **alias: Union[Column, str]) -> Select[S]:
        return Select(self._cnn).select(*columns, **alias)

    def insert[S: Schema](self, into: type[S], /) -> Insert[S]:
        return Insert(self._cnn).insert(into)

    def update[S: Schema](self, schema_t: type[S], /) -> Update[S]:
        return Update(self._cnn).update(schema_t)

    def delete[S: Schema](self, schema_t: type[S]) -> Delete[S]:
        return Delete(self._cnn).delete(schema_t)

    def __call__(self, query: str, args: Iterable[Any] = ()) -> Result:
        return Result(
            cnn=self._cnn,
            query=Query().update(query),
            args=Args().update(*args),
        )
