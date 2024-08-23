from __future__ import annotations

from typing import Any


class Args:
    def __init__(self):
        self._values: list = list()

    @classmethod
    def fr0m(cls, args: Args) -> Args:
        return Args().update(*args._values)

    def update(self, *values: Any) -> Args:
        for val in values:
            self._values.append(val)
        return self

    def parse(self) -> tuple[Any, ...]:
        return tuple(self._values)
