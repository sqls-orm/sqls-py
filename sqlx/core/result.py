from __future__ import annotations

from typing import Any, Optional

import aiomysql

from ..types import Schema, Query, Args, Row


class Result[S: Schema]:
    cursor_t: aiomysql.SSDictCursor

    def __init__(
            self,
            cnn: aiomysql.Connection,
            query: Optional[Query] = None,
            args: Optional[Args] = None,
    ):
        self._cnn: aiomysql.Connection = cnn
        self._query: Query = query or Query()
        self._args: Args = args or Args()

    def __await__(self):
        return self.execute().__await__()

    async def __aiter__(
            self,
            into: type[S] = Row,
    ) -> Any:
        async with self._cnn.cursor(self.cursor_t) as cursor:
            await cursor.execute(self._query.parse(), self._args.parse())
            async for row in cursor:
                yield into(**row)

    async def all(
            self,
            into: type[S] = Row,
            /,
    ) -> list[S]:
        async with self._cnn.cursor(self.cursor_t) as cursor:
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except Exception as e:
                await self._cnn.rollback()
                raise Exception(f'Failed {self._query.parse()} with {self._args.parse()}, since: "{e}"')
            return [into(**row) async for row in cursor]

    async def first(
            self,
            into: type[S] = Row,
            /,
    ) -> Optional[S]:
        async with self._cnn.cursor(self.cursor_t) as cursor:
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except Exception as e:
                await self._cnn.rollback()
                raise Exception(f'Failed {self._query.parse()} with {self._args.parse()}, since: "{e}"')
            return into(**row) if (row := cursor.fetchone) else None

    async def execute(self) -> None:
        async with self._cnn.cursor(self.cursor_t) as cursor:
            try:
                await cursor.execute(self._query.parse(), self._args.parse())
                await self._cnn.commit()
            except Exception as e:
                await self._cnn.rollback()
                raise Exception(f'Failed {self._query.parse()} with {self._args.parse()}, since: "{e}"')
