from __future__ import annotations

from .. import mixin
from ...types import Schema


class InsertQuery[S: Schema](
    mixin.IntoMixin,
    mixin.ValuesMixin,
    mixin.ReturningMixin,
):
    ...
    # def insert(self) -> Self:
    #     self._query.update('INSERT')
    #     return self
