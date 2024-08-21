from __future__ import annotations

from typing import Self

from ..result import Result
from ...types import Schema


class Offset[S: Schema](Result):
    def offset(
            self,
            offset: int,
            /,
    ) -> Self[S]:
        """

        :param offset:
        :return:
        """
        if not offset >= 0:
            raise ValueError(f'`.offset({offset}) must be >= 0`')

        self._query.update(f'OFFSET {offset}')

        return self
