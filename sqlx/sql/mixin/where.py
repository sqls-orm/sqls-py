from __future__ import annotations

from typing import Any, Union, Self, overload

from sqlx.core.result import Result
from ...types import Column, Schema


class WhereMixin(Result):
    @overload
    def where(
            self,
            conditions: Column,
    ) -> Self:
        """
        >>> .where((Schema.model().col1 == val1) & (Schema.model().col1 == val1))
        >>> .where((Schema.model().col1 == val1) | (Schema.model().col1 == val1))
        :param conditions:
        :return:
        """

    @overload
    def where(
            self,
            conditions: dict[Union[Column, str], Any],
    ) -> Self:
        """
        >>> .where({Schema.model().column: value})
        :param conditions:
        :return:
        """

    @overload
    def where(
            self,
            **conditions: Any,
    ) -> Self:
        """
        >>> .where(column=value)
        :param conditions:
        :return:
        """

    def where(
            self,
            as_dict_or_col: Union[
                dict[Union[Column, str], Any],
                Column,
            ] = None,
            **as_kwargs: Any,
    ) -> Self:
        if isinstance(as_dict_or_col, dict):
            as_dict = as_dict_or_col
            if len(as_dict) > 1:
                raise ValueError(f"I'm a teapot, don't u c? {as_dict}")
            conditions = ''.join(f'`{column}` = %s' for column in as_dict.keys())
            values = as_dict.values()
        elif isinstance(as_dict_or_col, Column):
            as_col = as_dict_or_col
            conditions = as_col
            values = as_col.args._values
        elif as_kwargs:
            as_dict = as_kwargs
            conditions = ''.join(f'`{column}` = %s' for column in as_dict.keys())
            values = as_dict.values()
        else:
            raise NotImplementedError('Most likely, invalid usage of `sqlx.where`')

        self._query.update(f'WHERE {conditions}')
        self._args.update(*values)

        return self
