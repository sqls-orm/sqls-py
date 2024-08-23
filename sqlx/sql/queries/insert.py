from __future__ import annotations

from typing import Self, overload, Any, Optional, Union

from .. import mixin
from ...types import Schema, Column


class InsertQuery(
    mixin.IntoMixin,
    mixin.ValuesMixin,
    mixin.ReturningMixin,
):
    # def insert(self) -> Self:
    #     self._query.update('INSERT')
    #     return self

    def on_duplicate(self) -> Self:
        self._query.update('ON DUPLICATE KEY')
        return self

    def ignore(self) -> Self:
        self._query._parts[0] = 'INSERT IGNORE'
        return self

    @overload
    def update(
            self,
            **values: Any,
    ) -> Self:
        """
        >>> .set(column=value)
        :param values:
        :return:
        """

    @overload
    def update(
            self,
            values: dict[Union[Column, str], Any],
    ) -> Self:
        """
        >>> .set({Schema.model().column: value})
        :param values:
        :return:
        """

    def update(
            self,
            args: Optional[dict[Union[Column, str], Any]] = None,
            **kwargs: Any,
    ) -> Self:
        if args and kwargs:
            __values = args | kwargs
        elif args:
            __values = args
        else:
            __values = kwargs

        columns: str = ', '.join(f'`{col}` = %s' for col in __values.keys())
        self._query.update(f'UPDATE {columns}')
        self._args.update(*__values.values())
        return self
