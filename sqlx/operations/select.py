from __future__ import annotations

from typing import Union, Iterable

from .result import Result
from .common import Where
from ..types import Schema, Column


class Select[S: Schema](Where, Result):
    def select(self, *columns: Iterable[Union[Column, str]], **alias: dict[str, Union[Column, str]]) -> Select[S]:
        # .select(Schema.model().column) -> {column: value_of(Schema.column)}
        # .select(alias=Schema.model().column) -> {alias: value_of(Schema.column)}
        columns = ', '.join((
            ', '.join(f'`{column}`' for column in columns),
            ', '.join(f'`{column}` AS `{column}`' for column in alias),
        )).strip(', ')
        self._query.update(f'SELECT {columns}')
        return self

    def fr0m(self, schema_t: type[S]) -> Select[S]:
        self._query.update(f'FROM `{schema_t.__table__}`')
        return self
