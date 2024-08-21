from __future__ import annotations

from typing import Self

from .. import mixin
from ...types import Schema


class Insert[S: Schema](
    mixin.Into,
    mixin.Values,
    mixin.Returning,
):
    def insert(self) -> Self[S]:
        self._query.update('INSERT')
        return self
