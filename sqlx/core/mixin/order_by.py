from __future__ import annotations

from typing import Union, overload, Self

from ..result import Result
from ...types import Column, Schema


class OrderBy[S: Schema](Result):
    @overload
    def order_by(
            self,
            *columns: Column,
    ) -> Self[S]:
        """
        >>> .order_by(Schema.col1.asc(), Schema.col2.desc())
        :param columns:
        :return:
        """

    @overload
    def order_by(
            self,
            *columns: str,
    ) -> Self[S]:
        """
        >>> .order_by(col1, col2)
        :param columns:
        :return:
        """

    @overload
    def order_by(
            self,
            **columns: str,
    ) -> Self[S]:
        """
        >>> .order_by(col1='asc', col2='desc')
        :param columns:
        :return:
        """

    def order_by(
            self,
            *args: Union[
                Column,
                str,
            ],
            **kwargs: str,
    ) -> Self[S]:
        if args:
            columns = ', '.join(f'`{column}`' for column in args)
        elif kwargs:
            columns = ', '.join(f'`{column}` {order.upper()}' for column, order in kwargs.items())
        else:
            raise NotImplementedError('No matching @overload found for `sqlx.order_by(...)`')

        self._query.update(f'ORDER BY {columns}')

        return self
