from __future__ import annotations

from typing import Any, Union, Self, overload, Optional, Literal

from ..result import Result
from ...types import Column, Schema


class Where[S: Schema](Result):
    @overload
    def where(self, conditions: Union[Column, str], /) -> Self[S]:
        """
        .where((Schema.model().col1 == val1) & (Schema.model().col1 == val1))
        .where((Schema.model().col1 == val1) | (Schema.model().col1 == val1))
        """

    @overload
    def where(self, conditions: dict[Union[Column, str], Any]) -> Self[S]:
        """
        .where({Schema.model().column: value})
        """

    @overload
    def where(self, **conditions: Any) -> Self[S]:
        """
        .where(column=value)
        """

    def where(
            self,
            conditions: Union[
                Union[Column, str],
                dict[Union[Column, str], Any],
            ] = None,
            **_conditions: Any,
    ) -> Self[S]:
        if isinstance(conditions, Column):
            __conditions = f'WHERE {conditions.value}'
            __args = conditions.args._values
        else:
            conditions = conditions or _conditions
            __conditions = f'WHERE {', '.join(f'`{column}` = %s' for column in conditions.keys())}'
            __args = conditions.values()
        self._query.update(f'WHERE {__conditions}')
        self._args.update(*__args)
        return self

    def __where(
            self,
            on: Literal['AND', 'OR', '_'],
            conditions: dict[Union[Column, Any]] = None,
            **_conditions: Any,
    ) -> Self[S]:
        if conditions and _conditions:
            __conditions = conditions | _conditions
        if conditions:
            __conditions = conditions
        elif _conditions:
            __conditions = _conditions
        self._args.update(*__conditions.values())
        self._query.update(f'WHERE {f' {on} '.join(f'`{column}` = %s' for column in __conditions.keys())}')
        return self

    @overload
    def where_and(self, **conditions: Any) -> Self[S]:
        """
        .where_and(col1=val1, col2=val2)
        """

    @overload
    def where_and(self, conditions: dict[Union[Column, Any]]) -> Self[S]:
        """
        .where_and({Schema.model().col1: val1, Schema.model().col2: val2})
        """

    def where_and(
            self,
            conditions: dict[Union[Column, Any]] = None,
            **_conditions: Any,
    ) -> Self[S]:
        self.__where('AND', conditions, **_conditions)
        return self

    @overload
    def where_or(self, **conditions: Any) -> Self[S]:
        """
        .where_and(col1=val1, col2=val2)
        """

    @overload
    def where_or(self, conditions: dict[Union[Column, Any]]) -> Self[S]:
        """
        .where_and({Schema.model().col1: val1, Schema.model().col2: val2})
        """

    def where_or(
            self,
            conditions: dict[Union[Column, Any]] = None,
            **_conditions: Any,
    ) -> Self[S]:
        self.__where('OR', conditions, **_conditions)
        return self
