from __future__ import annotations

from typing import Union, Any, Iterable, overload

from .common import Returning
from .result import Result
from ..types import Schema, Column


class Insert[S: Schema](Returning, Result):
    def insert[S: Schema](self, schema_t: type[S]) -> Insert[S]:
        self._query.update(f'INSERT INTO `{schema_t.__table__}`')
        return self

    @overload
    def values(
            self,
            **values: Any,
    ) -> Insert[S]:
        """
        .values(col1=val1, col2=val2)
        """

    @overload
    def values(
            self,
            values: dict[Union[Column, str], Any],
    ) -> Insert[S]:
        """
        .values({Schema.model().col1: val1, Schema.model().col2: val2})
        """

    @overload
    def values(
            self,
            values: Iterable[dict[Union[Column, str], Any]],
    ) -> Insert[S]:
        """
        .values([
            {Schema.model().col1: val1, Schema.model().col2: val2},
            {Schema.model().col1: val3, Schema.model().col2: val4},
        ])
        .values([
            dict(col1=val1, col2=val2),
            dict(col1=val3, col2=val4),
        ])
        """

    def values(
            self,
            values: Union[
                dict[Union[Column, str], Any],
                Iterable[dict[Union[Column, str], Any]]
            ] = (),
            **_values: Union[Column, str],
    ) -> Insert[S]:
        # TODO
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
