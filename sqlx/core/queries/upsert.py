from __future__ import annotations

from typing import Self

from .. import mixin
from ...types import Schema


class Upsert[S: Schema](
    mixin.Into,
    mixin.Values,
    mixin.Returning,
):
    def upsert(self) -> Self[S]:
        self._query.update('REPLACE')
        return self
