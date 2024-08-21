from __future__ import annotations

from typing import Self

from ..result import Result
from ...types import Schema


class Limit[S: Schema](Result):
    def limit(
            self,
            limit: int,
            /,
    ) -> Self[S]:
        """

        :param limit:
        :return:
        """
        if not limit > 0:
            raise ValueError(f'`.limit({limit}) must be > 0`')

        self._query.update(f'LIMIT {limit}')

        return self
