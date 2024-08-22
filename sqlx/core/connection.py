from __future__ import annotations

from typing import Optional

import aiomysql

from sqlx.sql.vendor import SQLVendor


class ConnectionManager(SQLVendor):
    def __init__(
            self,
            pool: aiomysql.Pool,
            cnn: Optional[aiomysql.pool._PoolAcquireContextManager] = None
    ):
        print((pool, cnn))
        self.pool: aiomysql.Pool = pool
        self.cnn: Optional[aiomysql.pool._PoolAcquireContextManager] = cnn

    async def __aenter__(self) -> aiomysql.Connection:
        print(self.cnn)
        if self.cnn:
            async with self.cnn as cnn:
                print('got', type(cnn))
                return cnn
        async with self.pool.acquire() as cnn:
            print('got', type(cnn))
            return cnn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @property
    def default(self) -> ConnectionManager:
        return ConnectionManager(pool=self.pool)
