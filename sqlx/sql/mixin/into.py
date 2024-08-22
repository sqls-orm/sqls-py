from __future__ import annotations

from typing import Union, overload, Self

from sqlx.core.result import Result
from ...types import Schema


class IntoMixin[S: Schema](Result):
    @overload
    def into(
            self,
            table: type[S],
    ) -> Self:
        """
        >>> .into(Schema)
        :param table:
        :return:
        """

    @overload
    def into(
            self,
            table: str,
    ) -> Self:
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
    ) -> Self:
        if isinstance(table, str):
            table = table
        elif issubclass(table, Schema):
            table = table.__table__
        else:
            raise NotImplementedError('No matching @overload found for `sqlx.into(...)`')

        self._query.update(f'INTO `{table}`')

        return self
