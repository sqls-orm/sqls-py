from __future__ import annotations

import aiomysql

from .connection import ConnectionManager
from sqlx.sql.vendor import SQLVendor


class SQLX(SQLVendor):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    async def create_pool(self) -> None:
        self.pool = await aiomysql.create_pool(*self.args, **self.kwargs)

    async def close_pool(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    def __del__(self) -> None:
        self.pool.close()
