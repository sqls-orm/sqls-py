from __future__ import annotations

from typing import Any, Optional, Iterable

import aiomysql

from sqlx.types import Schema, Query, Args, Row


class Result[S: Schema]:
    def __init__(
            self,
            cnnmgr: 'ConnectionManager',
            query: str,
            args: Iterable[Any] = (),
    ):
        self._cnnmgr: 'ConnectionManager' = cnnmgr
        self._query: Query = Query().update(query)
        self._args: Args = Args().update(*args)

    def __await__(self):
        return self.execute().__await__()

    async def __aenter__(self) -> tuple[type[aiomysql.Cursor], aiomysql.Connection]:
        async with self._cnnmgr as cnn:
            async with cnn.cursor(aiomysql.SSDictCursor) as cursor:
                return cursor, cnn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    async def __aiter__(
            self,
            into: type[S] = Row,
    ) -> Any:
        async with self as (cursor, _):
            await cursor.execute(self._query.parse(), self._args.parse())
            async for row in cursor:
                yield into(**row)

    async def all(
            self,
            into: type[S] = Row,
            /,
    ) -> list[S]:
        # async with self as (cursor, cnn):
        async with self._cnnmgr as cnn:
            async with cnn.cursor(aiomysql.SSDictCursor) as cursor:
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await cnn.commit()
                except Exception as e:
                    await cnn.rollback()
                    raise Exception(f'Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}"')
                return [into(**row) async for row in cursor]

    async def first(
            self,
            into: type[S] = Row,
            /,
    ) -> Optional[S]:
        async with self as (cursor, cnn):
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await cnn.commit()
            except Exception as e:
                await cnn.rollback()
                raise Exception(f'Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}"')
            return into(**row) if (row := await cursor.fetchone()) else None

    async def execute(self) -> None:
        async with self as (cursor, cnn):
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await cnn.commit()
            except Exception as e:
                await cnn.rollback()
                raise Exception(f'Failed "{self._query.parse()}" with "{self._args.parse()}", since: "{e}"')
