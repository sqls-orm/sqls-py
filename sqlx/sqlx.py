from __future__ import annotations

import asyncio

import aiomysql


class SQLX(aiomysql.pool.Pool):
    def __init__(
            self,
            minsize: int = 1,
            maxsize: int = 10,
            echo: bool = False,
            pool_recycle: int = -1,
            loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
            **kwargs,
    ):
        super().__init__(minsize, maxsize, echo, pool_recycle, loop, **kwargs)
        self.is_serving()
