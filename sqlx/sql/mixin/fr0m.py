from __future__ import annotations

from typing import Union, overload, Self

from sqlx.core.result import Result
from ...types import Schema


class FromMixin[S: Schema](Result):
    @overload
    def fr0m(
            self,
            table: str,
    ) -> Self:
        """
        >>> .fr0m('tablename')
        :param table:
        :return:
        """

    @overload
    def fr0m(
            self,
            table: type[S],
    ) -> Self:
        """
        >>> .fr0m(Schema)
        :param table:
        :return:
        """

    def fr0m(
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
            raise NotImplementedError('No mathing @overload found for `sqlx.fr0m(...)`')

        self._query.update(f'FROM {table}')

        return self
