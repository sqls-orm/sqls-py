from __future__ import annotations

from typing import Union, Any

from .result import Result
from .common import Where, Returning
from ..types import Schema, Column


class Update[S: Schema](Where, Returning, Result):
    def update(self, schema_t: type[S]) -> Update[S]:
        self._query.update(f'UPDATE `{schema_t.__table__}`')
        return self

    def set(self, values: dict[Union[Column, str], Any]) -> Update[S]:
        columns: str = ', '.join(f'`{col}` = %s' for col in values.keys())
        self._query.update(f'SET {columns}')
        self._args.update(*values.values())
        return self
