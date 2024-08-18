from __future__ import annotations

from typing import Union, Any, Iterable

from .common import Returning
from .result import Result
from ..types import Schema, Column


class Insert[S: Schema](Returning, Result):
    def insert[S: Schema](self, schema_t: type[S]) -> Insert[S]:
        self._query.update(f'INSERT INTO `{schema_t.__table__}`')
        return self

    def values(
            self,
            values: Union[dict[Union[Column, str], Any], Iterable[dict[Union[Column, str], Any]]] = (),
            **_values: Union[Column, str],
    ) -> Insert[S]:
        # .values(column=value)
        # .values([{column: value}, {column: value}])
        # .values({Schema.model().column: value})
        # .values([{Schema.model().column: value}, {Schema.model().column: value}])
        if isinstance(values, dict):
            values |= _values
            columns: str = ', '.join(f'`{col}`' for col in values.keys())
            placeholders: str = ', '.join('%s' for _ in range(len(values)))
        elif values:
            columns: str = ', '.join(f'`{col}`' for col in values[0].keys())
            placeholders = ', '.join(', '.join('%s' for _ in range(len(set))) for set in values)
        else:
            values = _values
            columns: str = ', '.join(f'`{col}`' for col in values.keys())
            placeholders: str = ', '.join('%s' for _ in range(len(values)))
        self._query.update(f'({columns}) VALUES ({placeholders})')
        self._args.update(*values.values())
        return self
