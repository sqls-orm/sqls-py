from __future__ import annotations

from typing import Union, overload, Self

from ..result import Result
from ...types import Column, Schema


class Into[S: Schema](Result):
    @overload
    def into(
            self,
            table: type[S],
    ) -> Self[S]:
        """
        >>> .into(Schema)
        :param table:
        :return:
        """

    @overload
    def into(
            self,
            table: str,
    ) -> Self[S]:
        """
        >>> .into('table')
        :param table:
        :return:
        """

    def into(
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
            raise NotImplementedError('No matching @overload found for `sqlx.into(...)`')

        self._query.update(f'INTO `{table}`')

        return self