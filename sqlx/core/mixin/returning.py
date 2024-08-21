from __future__ import annotations

from typing import Union, overload, Self

from ..result import Result
from ...types import Column, Schema


class Returning[S: Schema](Result):
    @overload
    def returning(
            self,
            *columns: Union[Column, str],
    ) -> Self[S]:
        """
        >>> .returning('col1', 'col2')
        >>> .returning('col1', Schema.model().col2)
        >>> .returning(Schema.model().col1, Schema.model().col2)
        :param columns:
        :return:
        """

    @overload
    def returning(
            self,
            **alias: Union[Column, str],
    ) -> Self[S]:
        """
        >>> .returning(alias1='col1', alias2='col2')
        >>> .returning(alias1='col1', alias2=Schema.model().col2)
        >>> .returning(alias1=Schema.model().col1, alias2=Schema.model().col2)
        :param alias:
        :return:
        """

    def returning(
            self,
            *args: Union[Column, str],
            **kwargs: Union[Column, str],
    ) -> Self[S]:
        columns = ', '.join((
            ', '.join(f'`{column}`' for column in args),
            ', '.join(f'`{column}` AS `{alias}`' for alias, column in kwargs.items()),
        )).strip(', ') or '*'
        self._query.update(f'RETURNING {columns}')
        return self
