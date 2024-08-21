from __future__ import annotations

from typing import Self

from ...types import Schema
from .. import mixin


class Delete[S: Schema](
    mixin.From,
    mixin.Where,
    mixin.Returning,
):
    def delete(self) -> Self[S]:
        self._query.update('DELETE')
        return self
