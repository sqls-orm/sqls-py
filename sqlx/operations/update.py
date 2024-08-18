from __future__ import annotations

from typing import Union, Any, overload, Optional

from .result import Result
from .common import Where, Returning
from ..types import Schema, Column


class Update[S: Schema](Where, Returning, Result):
    def update(self, schema_t: type[S]) -> Update[S]:
        self._query.update(f'UPDATE `{schema_t.__table__}`')
        return self

    @overload
    def set(self, **values: Any) -> Update[S]:
        """
        .set(column=value)
        """

    @overload
    def set(self, values: dict[Union[Column, str], Any]) -> Update[S]:
        """
        .set({Schema.model().column: value})
        """

    def set(
            self,
            values: Optional[dict[Union[Column, str], Any]] = None,
            **_values: Any,
    ) -> Update[S]:
        if values and _values:
            __values = values | _values
        elif values:
            __values = values
        else:
            __values = _values

        columns: str = ', '.join(f'`{col}` = %s' for col in __values.keys())
        self._query.update(f'SET {columns}')
        self._args.update(*__values.values())
        return self
