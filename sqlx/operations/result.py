from __future__ import annotations

from typing import Any, Optional

import aiomysql
import pymysql

from ..types import Schema, Query, Args, Row


class Result[S: Schema]:
    def __init__(
            self,
            cnn: aiomysql.Connection,
            query: Optional[Query] = None,
            args: Optional[Args] = None,
    ):
        self._cnn: aiomysql.Connection = cnn
        self._query: Query = query or Query()
        self._args: Args = args or Args()

    async def __aiter__(self) -> Any:
        print((self._query.parse(), self._args.parse()))
        async with self._cnn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            await cursor.execute(self._query.parse(), self._args.parse())
            while record := await cursor.fetchone():
                yield Row(record)

    async def __anext__(self):
        """TODO"""

    # async def all(self) -> list[Row[str, Any]]:
    async def all(self) -> list[S]:
        print((self._query.parse(), self._args.parse()))
        async with self._cnn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except pymysql.err.Error as e:
                await self._cnn.rollback()
                raise e
            return [Row(row) for row in await cursor.fetchall()]

    # async def one(self) -> Row:
    async def one(self) -> S:
        print((self._query.parse(), self._args.parse()))
        async with self._cnn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except pymysql.err.Error as e:
                await self._cnn.rollback()
                raise e
            return Row(await cursor.fetchone() or dict())

    async def exec(self) -> int:
        print((self._query.parse(), self._args.parse()))
        async with self._cnn.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except pymysql.err.Error as e:
                await self._cnn.rollback()
                raise e
            return cursor.lastrowid or cursor.rowcount
