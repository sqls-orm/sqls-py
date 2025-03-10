from __future__ import annotations

from typing import Union, overload, Self

from sqls.core.result import Result
from ...types import Schema


class IntoMixin(Result):
    @overload
    def into(
            self,
            table: type[Schema],
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
                type[Schema],
                str,
            ],
    ) -> Self:
        if isinstance(table, str):
            ...
        elif table := getattr(table, '__table__', None):
            ...
        else:
            raise NotImplementedError('No matching @overload found for `sqls.into(...)`')

        self._query.update(f'INTO `{table}`')

        return self
