from __future__ import annotations

from typing import Any, Union, Self, overload, Optional, Literal

from ..result import Result
from ...types import Column, Schema


class Where[S: Schema](Result):
    @overload
    def where(self, condition: Union[Column, str], /) -> Self[S]:
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
            condition: Union[Column, str],
            conditions: dict[Union[Column, str], Any],
            **_conditions: Any,
    ) -> Self[S]:
        # TODO
        self._query.update(f'WHERE {conditions.value}')
        self._args.update(*conditions.args._values)
        return self

    def __where(
            self,
            on: Literal['AND', 'OR', '_'],
            conditions: Optional[dict[Union[Column, Any]]] = None,
            **_conditions: Any,
    ) -> Self[S]:
        # TODO
        self._args.update(*conditions.values())
        conditions: str = f' {on} '.join(conditions.keys())
        self._query.update(f'WHERE {conditions}')
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
            conditions: Optional[dict[Union[Column, Any]]] = None,
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
            conditions: Optional[dict[Union[Column, Any]]] = None,
            **_conditions: Any,
    ) -> Self[S]:
        self.__where('OR', conditions, **_conditions)
        return self
