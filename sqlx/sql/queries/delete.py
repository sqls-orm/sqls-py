from __future__ import annotations

from .. import mixin
from ...types import Schema


class DeleteQuery[S: Schema](
    mixin.FromMixin,
    mixin.WhereMixin,
    mixin.ReturningMixin,
):
    ...
    # def delete(self) -> Self:
    #     self._query.update('DELETE')
    #     return self
