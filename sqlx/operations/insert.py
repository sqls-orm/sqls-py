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
            ] = None,
            **_values: Union[Column, str],
    ) -> Insert[S]:
        if isinstance(values, dict) or _values:
            __values = values | _values if values else _values
            columns: str = ', '.join(f'`{col}`' for col in __values.keys())
            placeholders: str = ', '.join('%s' for _ in range(len(__values)))
            __args = __values.values()
        elif isinstance(values, Iterable):
            __values = values
            columns: str = ', '.join(f'`{col}`' for col in __values[0].keys())
            placeholders = ', '.join(f'({', '.join('%s' for _ in range(len(set)))})' for set in __values)
            __args = [arg for arg in [set for set in __values]]
        self._query.update(f'({columns}) VALUES ({placeholders})')
        self._args.update(*__args)
        return self
