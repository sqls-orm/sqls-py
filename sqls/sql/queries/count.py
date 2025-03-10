from __future__ import annotations

from typing import Generator, Any

from .. import mixin
from ...types import Schema


class CountQuery(
    mixin.JoinMixin,
    mixin.WhereMixin,
):
    def __await__(self) -> Generator[Any, None, int]:
        async def wrapper() -> int:
            row = await self.first()
            return row['total']

        return wrapper().__await__()
