from __future__ import annotations

from typing import Any, Optional

from .args import Args


class Column:
    def __init__(self, name: str, args: Optional[Args] = None):
        self.value: str = name
        self.args: Args = args or Args()

    def __hash__(self) -> int:
        return hash(self.value)

    def __or__(self, other: Column) -> Column:
        return Column(f'({self.value}) OR ({other.value})')

    def __and__(self, other: Column) -> Column:
        return Column(f'({self.value}) AND ({other.value})')

    def __eq__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` = %s', self.args)

    def __ne__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` != %s', self.args)

    def __lt__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` < %s', self.args)

    def __le__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` <= %s', self.args)

    def __gt__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` > %s', self.args)

    def __ge__(self, value: Any) -> Column:
        self.args.update(value)
        return Column(f'`{self.value}` => %s', self.args)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
