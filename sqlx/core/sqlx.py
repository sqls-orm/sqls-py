from __future__ import annotations

import aiomysql

from .connection import ConnectionManager
from sqlx.sql.vendor import SQLVendor


class SQLX(SQLVendor):
    def __init__(self, pool: aiomysql.Pool):
        self.pool: aiomysql.Pool = pool

    @classmethod
    async def create_pool(cls, *args, **kwargs) -> SQLX:
        return SQLX(pool=await aiomysql.create_pool(*args, **kwargs))

    async def close_pool(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()

    def __del__(self) -> None:
        self.pool.close()
