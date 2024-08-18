from __future__ import annotations

import aiomysql

from .operations import Connection


class SQLX:
    def __init__(self, pool: aiomysql.Pool):
        self._pool: aiomysql.Pool = pool

    async def __aenter__(self) -> Connection:
        async with self._pool.acquire() as cnn:
            return Connection(cnn=cnn)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
