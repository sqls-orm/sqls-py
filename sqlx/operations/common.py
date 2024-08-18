from __future__ import annotations

from typing import Any, Union, Self

from .result import Result
from ..types import Column, Schema


class Returning[S: Schema](Result):
    def returning(self, *columns: Union[Column, str], **alias: Union[Column, str]) -> Returning[S]:
        # .returning(Schema.model().column) -> {column: value_of(Schema.column)}
        # .returning(alias=Schema.model().column) -> {alias: value_of(Schema.column)}
        columns: str = ', '.join((
            ', '.join(f'`{column}`' for column in columns),
            ', '.join(f'`{column}` AS `{column}`' for column in alias),
        )).strip(', ')
        self._query.update(f'RETURNING {columns}')
        return self


class Where[S: Schema](Result):
    def where(self, conditions: Union[Column, str]) -> Self[S]:
        self._query.update(f'WHERE {conditions.value}')
        self._args.update(*conditions.args._values)
        return self

    def where_and(self, **conditions: Any) -> Self[S]:
        # TODO
        self._args.update(*conditions.values())
        conditions: str = ' AND '.join(conditions.keys())
        self._query.update(f'WHERE {conditions}')
        return self

    def where_or(self, **conditions: Any) -> Self[S]:
        # TODO
        self._args.update(*conditions.values())
        conditions: str = ' OR '.join(conditions.keys())
        self._query.update(f'WHERE {conditions}')
        return self
