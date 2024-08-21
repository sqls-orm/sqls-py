from __future__ import annotations

from typing import Union, Any, overload, Optional, Self

from .. import mixin
from ...types import Schema, Column


class Update[S: Schema](
    mixin.Where,
    mixin.Returning,
):
    @overload
    def update(
            self,
            table: type[S],
    ) -> Self[S]:
        """
        >>> .update(Schema)
        :param table:
        :return:
        """

    @overload
    def update(
            self,
            table: str,
    ) -> Self[S]:
        """
        >>> .update('table')
        :param table:
        :return:
        """

    @overload
    def update(
            self,
            table: Union[
                type[S],
                str,
            ],
    ) -> Self[S]:
        if isinstance(table, str):
            table = table
        elif issubclass(table, Schema):
            table = table.__table__
        else:
            raise NotImplementedError('No matching @overload found for `sqlx.update(...)`')

        self._query.update(f'UPDATE {table}')

        return self

    @overload
    def set(
            self,
            **values: Any,
    ) -> Self[S]:
        """
        >>> .set(column=value)
        :param values:
        :return:
        """

    @overload
    def set(
            self,
            values: dict[Union[Column, str], Any],
    ) -> Self[S]:
        """
        >>> .set({Schema.model().column: value})
        :param values:
        :return:
        """

    def set(
            self,
            args: Optional[dict[Union[Column, str], Any]] = None,
            **kwargs: Any,
    ) -> Self[S]:
        if args and kwargs:
            __values = args | kwargs
        elif args:
            __values = args
        else:
            __values = kwargs

        columns: str = ', '.join(f'`{col}` = %s' for col in __values.keys())
        self._query.update(f'SET {columns}')
        self._args.update(*__values.values())
        return self
