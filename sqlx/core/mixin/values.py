from __future__ import annotations

from typing import Self, overload, Union, Any, Iterable

from ..result import Result
from ...types import Schema, Column


class Values[S: Schema](Result):
    @overload
    def values(
            self,
            **values: Any,
    ) -> Self[S]:
        """
        >>> .values(col1=val1, col2=val2)
        """

    @overload
    def values(
            self,
            values: dict[Union[Column, str], Any],
    ) -> Self[S]:
        """
        >>> .values({col1: val1, Schema.model().col2: val2})
        """

    @overload
    def values(
            self,
            values: Iterable[dict[Union[Column, str], Any]],
    ) -> Self[S]:
        """
        >>> .values([
        >>>     {Schema.model().col1: val1, Schema.model().col2: val2},
        >>>     {Schema.model().col1: val3, Schema.model().col2: val4},
        >>> ])
        >>> .values([
        >>>     dict(col1=val1, col2=val2),
        >>>     dict(col1=val3, col2=val4),
        >>> ])
        >>> .values([
        >>>     {col1: val1, col2: val2},
        >>>     {col1: val3, col2: val4},
        >>> ])
        """

    def values(
            self,
            as_dict_or_many: Union[
                dict[Union[Column, str], Any],
                Iterable[dict[Union[Column, str], Any]],
            ] = None,
            **kwargs: Union[Column, str],
    ) -> Self[S]:
        if isinstance(as_dict_or_many, dict):
            as_dict = as_dict_or_many
            columns = ', '.join(f'`{col}`' for col in as_dict.keys())
            placeholders = f'({', '.join('%s' for _ in range(len(as_dict)))})'
            values = as_dict.values()
        elif isinstance(as_dict_or_many, Iterable):
            as_many = as_dict_or_many
            columns = ', '.join(f'`{col}`' for col in next(iter(as_many)).keys())
            placeholders = ', '.join(f'({', '.join('%s' for _ in range(len(set)))})' for set in as_many)
            values = [arg for set in as_many for arg in set.values()]
        elif kwargs:
            columns = ', '.join(f'`{col}`' for col in kwargs.keys())
            placeholders = f'({', '.join('%s' for _ in range(len(kwargs)))})'
            values = kwargs.values()
        else:
            columns = ''
            placeholders = '()'
            values = ()

        self._query.update(f'({columns}) VALUES {placeholders}')
        self._args.update(*values)

        return self
