from __future__ import annotations

from typing import Union, overload, Self, Literal

from sqlx.core.result import Result
from ...types import Column, Schema


class JoinMixin[S: Schema](Result):
    @overload
    def join(
            self,
            table: str,
            *,
            type: Literal['INNER', 'LEFT', 'RIGHT', 'CROSS'] = 'INNER',
    ) -> Self:
        """
        >>> .join('tablename')
        :param table:
        :param type:
        :return:
        """

    @overload
    def join(
            self,
            table: type[S],
            *,
            type: Literal['INNER', 'LEFT', 'RIGHT', 'CROSS'] = 'INNER',
    ) -> Self:
        """
        >>> .join(Schema)
        :param table:
        :param type:
        :return:
        """

    def join(
            self,
            table: Union[
                type[S],
                str,
            ],
            *,
            type: Literal['INNER', 'LEFT', 'RIGHT', 'CROSS'] = 'INNER',
    ) -> Self:
        if isinstance(table, str):
            table = table
        elif issubclass(table, Schema):
            table = table.__table__
        else:
            raise NotImplementedError('No matching @overload found for `sqlx.join(...)`')

        self._query.update(f'{type} JOIN {table}')

        return self

    @overload
    def on(
            self,
            on: str,
            /,
    ):
        """
        >>> .on('table1.col = table2.col')
        :param on:
        :return:
        """

    @overload
    def on(
            self,
            on: Column,
            /,
    ):
        """
        >>> .on(Schema1.col == Schema2.col)
        :param on:
        :return:
        """

    @overload
    def on(
            self,
            on: Union[
                Column,
                str,
            ],
            /,
    ):
        if not isinstance(on, (str, Column)):
            raise NotImplementedError('No matching @overload found for `sqlx.on(...)`')

        self._query.update(f'ON {on}')

        return self
