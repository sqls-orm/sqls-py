from __future__ import annotations

from typing import Any, Optional, Iterable

import aiomysql

from sqlx.types import Schema, Query, Args, Row


class Result:
    def __init__(
            self,
            pool: aiomysql.Pool,
            query: str,
            args: Iterable[Any] = (),
    ):
        self._pool: aiomysql.Pool = pool
        self._query: Query = Query().update(query)
        self._args: Args = Args().update(*args)

    def __await__(self):
        return self.execute().__await__()

    async def __aiter__(
            self,
            into: type[Schema] = Row,
    ) -> Any:
        async with self._pool.acquire() as cnn:
            async with cnn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(self._query.parse(), self._args.parse())
                async for row in cursor:
                    yield into(**row)

    async def all(
            self,
            into: type[Schema] = Row,
            /,
    ) -> list[Schema]:
        async with self._pool.acquire() as cnn:
            async with cnn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await cnn.commit()
                except Exception as e:
                    await cnn.rollback()
                    raise Exception(f'"Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}""')
                return [into(**row) async for row in cursor]

    async def first(
            self,
            into: type[Schema] = Row,
            /,
    ) -> Optional[Schema]:
        async with self._pool.acquire() as cnn:
            async with cnn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await cnn.commit()
                except Exception as e:
                    await cnn.rollback()
                    raise Exception(f'"Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}""')
                return into(**row) if (row := await cursor.fetchone()) else None

    async def execute(self) -> None:
        async with self._pool.acquire() as cnn:
            async with cnn.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await cnn.commit()
                except Exception as e:
                    await cnn.rollback()
                    raise Exception(f'"Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}""')
