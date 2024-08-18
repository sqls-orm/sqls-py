from __future__ import annotations

from .common import Where, Returning
from ..types import Schema


class Delete[S: Schema](Where, Returning):
    def delete(self, schema_t: type[S]) -> Delete[S]:
        self._query.update(f'DELETE FROM `{schema_t.__table__}`')
        return self
