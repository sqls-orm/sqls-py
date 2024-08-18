from __future__ import annotations

from typing import Union, overload

from ..result import Result
from ...types import Column, Schema


class Returning[S: Schema](Result):
    @overload
    def returning(self, *columns: Union[Column, str]) -> Returning[S]:
        """
        .returning('col1', 'col2')
        .returning('col1', Schema.model().col2)
        .returning(Schema.model().col1, Schema.model().col2)
        """

    @overload
    def returning(self, **alias: Union[Column, str]) -> Returning[S]:
        """
        .returning(alias1='col1', alias2='col2')
        .returning(alias1='col1', alias2=Schema.model().col2)
        .returning(alias1=Schema.model().col1, alias2=Schema.model().col2)
        """

    def returning(
            self,
            *columns: Union[Column, str],
            **alias: Union[Column, str],
    ) -> Returning[S]:
        # .returning(Schema.model().column) -> {column: value_of(Schema.column)}
        # .returning(alias=Schema.model().column) -> {alias: value_of(Schema.column)}
        columns: str = ', '.join((
            ', '.join(f'`{column}`' for column in columns),
            ', '.join(f'`{column}` AS `{column}`' for column in alias),
        )).strip(', ')
        self._query.update(f'RETURNING {columns}')
        return self
