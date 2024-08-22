from __future__ import annotations

from typing import Any, Optional, overload, Union

from .args import Args


class Column:
    def __init__(self, name: str, args: Optional[Args] = None, *, table: Optional[str] = None):
        self.value: str = name
        self.args: Args = args or Args()
        self.table: Optional[str] = table

    def __hash__(self) -> int:
        return hash(self.value)

    def __or__(self, other: Column) -> Column:
        return Column(f'({self.value}) OR ({other.value})', self.args.update(*other.args._values))

    def __and__(self, other: Column) -> Column:
        return Column(f'({self.value}) AND ({other.value})', self.args.update(*other.args._values))

    @overload
    def __eq__(self, value: Column) -> Column:
        """
        >>> .join.on(Schema1.model().id == Schema2.model().schema1_id)
        :param value:
        :return:
        """

    @overload
    def __eq__(self, value: Any) -> Column:
        """
        >>> .where(Schema.model().col1 == val1)
        :param value:
        :return:
        """

    def __eq__(
            self,
            value: Union[
                Column,
                Any,
            ],
    ) -> Column:
        if isinstance(value, Column):
            return Column(f'`{self.table}.{self.value}` = `{value.table}.{value.value}`')
        return Column(f'`{self.value}` = %s', self.args.update(value))

    def __ne__(self, value: Any) -> Column:
        return Column(f'`{self.value}` != %s', self.args.update(value))

    def __lt__(self, value: Any) -> Column:
        return Column(f'`{self.value}` < %s', self.args.update(value))

    def __le__(self, value: Any) -> Column:
        return Column(f'`{self.value}` <= %s', self.args.update(value))

    def __gt__(self, value: Any) -> Column:
        return Column(f'`{self.value}` > %s', self.args.update(value))

    def __ge__(self, value: Any) -> Column:
        return Column(f'`{self.value}` => %s', self.args.update(value))

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def desc(self) -> str:
        return f'`{self.value}` DESC'

    def asc(self) -> str:
        return f'`{self.value}` ASC'
