from __future__ import annotations

from .. import mixin
from ...types import Schema


class UpsertQuery(
    mixin.IntoMixin,
    mixin.ValuesMixin,
    mixin.ReturningMixin,
):
    ...
    # def upsert(self) -> Self:
    #     self._query.update('REPLACE')
    #     return self
