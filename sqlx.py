from __future__ import annotations

import asyncio
from abc import abstractmethod
from typing import Any, Iterable, Optional, AsyncGenerator, Union

import aiomysql
import pymysql
from pydantic import BaseModel, Field


class Row(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = Row(v)

    def __getattr__(self, item: str) -> Any:
        if item in self:
            return self[item]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

    def __getattribute__(self, item: str) -> Any:
        try:
            return super().__getattribute__(item)
        except AttributeError:
            return self.__getattr__(item)

    def __setattr__(self, key: str, value: Any) -> None:
        self[key] = value


class Schema(BaseModel):
    @property
    @abstractmethod
    def __table__(self) -> str:
        ...


class Query:
    def __init__(self):
        self._parts: list[str] = list()

    def update(self, value: str) -> Query:
        self._parts.append(value)
        return self

    def parse(self) -> str:
        return f'{' '.join(self._parts)};'

class Args:
    def __init__(self):
        self._values: list = list()

    def update(self, *values: Any) -> Args:
        for val in values:
            self._values.append(val)
        return self

    def parse(self) -> tuple[Any, ...]:
        return tuple(self._values)


class Result[S: Schema]:
    def __init__(self, pool: aiomysql.Pool):
        self._pool: aiomysql.Pool = pool
        self._query: Query = Query()
        self._args: Args = Args()

    # async def all(self) -> list[Row[str, Any]]:
    async def all(self) -> list[S]:
        print((self._query.parse(), self._args.parse()))
        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await connection.commit()
                except pymysql.err.Error as e:
                    await connection.rollback()
                    raise e
                return [Row(row) for row in await cursor.fetchall()]

    # async def one(self) -> Row:
    async def one(self) -> S:
        print((self._query.parse(), self._args.parse()))
        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await connection.commit()
                except pymysql.err.Error as e:
                    await connection.rollback()
                    raise e
                return Row(await cursor.fetchone() or dict())

    # async def select(self) -> AsyncGenerator[Row[str, Any], None]:
    async def select(self) -> AsyncGenerator[S, None]:
        print((self._query.parse(), self._args.parse()))
        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                await cursor.execute(self._query.parse(), self._args.parse())
                while record := await cursor.fetchone():
                    yield Row(record)

    async def execute(self) -> None:
        print((self._query.parse(), self._args.parse()))
        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await connection.commit()
                except pymysql.err.Error as e:
                    await connection.rollback()
                    raise e

    async def count(self) -> int:
        print((self._query.parse(), self._args.parse()))
        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor
                try:
                    await cursor.execute(self._query.parse(), self._args.parse())
                    await connection.commit()
                except pymysql.err.Error as e:
                    await connection.rollback()
                    raise e
                return cursor.rowcount


class WhereLogical:
    def __init__(self, **condition: Any):
        self.conditions: dict[str, Any] = condition

    def __str__(self) -> str:
        col, value = self.conditions[: 1]
        return f'`{col}` = %s'

    def __or__(self, other):
        return f'({self} OR {other})'


class WhereClause[S: Schema](Result):
    def where(self, *logical: WhereLogical) -> WhereClause[S]:

        columns = ', '.join(f'`{col}` = %s' for col in conditions.keys())
        self._query.update(f'WHERE {columns}')
        self._args.update(*conditions.values())
        return self


class Insert[S: Schema](Result):
    def insert[S: Schema](self, schema_t: type[S]) -> Insert[S]:
        self._query.update(f'INSERT INTO {schema_t.__table__}')
        return self

    def values(self, **values: Any) -> Insert[S]:
        columns: str = ', '.join(f'`{col}`' for col in values.keys())
        placeholders: str = ', '.join(['%s'] * len(values))
        self._query.update(f'({columns}) VALUES ({placeholders})')
        self._args.update(*values.values())
        return self

    def returning(self, *columns: str) -> Insert[S]:
        columns: str = ', '.join(f'`{col}`' for col in columns)
        self._query.update(f'RETURNING {columns}')
        return self


class Update[S: Schema](WhereClause):
    def update(self, schema_t: type[S]) -> Update[S]:
        self._query.update(f'UPDATE {schema_t.__table__}')
        return self

    def set(self, **values: Any) -> Update[S]:
        columns: str = ', '.join(f'`{col}` = %s' for col in values.keys())
        self._query.update(f'SET {columns}')
        self._args.update(*values.values())
        return self


class SQLX:
    def __init__(self, pool: aiomysql.Pool):
        self._pool: aiomysql.Pool = pool

    def where(self, **conditions: Any):

    def insert[S: Schema](self, schema_t: type[S]) -> Insert[S]:
        return Insert(self._pool).insert(schema_t)

    def update[S: Schema](self, schema_t: type[S]) -> Update[S]:
        return Update(self._pool).update(schema_t)

    # def __call__(self, query: Query, args: Arguments) -> Result:
    #     return Result.of(
    #         pool=self._pool,
    #         query=query,
    #         args=args,
    #     )

    # def update[S: Schema](self, schema: type[S]) -> Update:
    #     return Update[S](
    #         pool=self._pool,
    #         query=f'UPDATE {schema.__table__}',
    #         args=Arguments(),
    #     )


class User(Schema):
    __table__ = '`user`'

    username: str = Field()
    password: str = Field()


async def main():
    sqlx = SQLX(pool=await aiomysql.create_pool(
        db='temp',
        user='admin',
        password='n1AIRSaPV8EDx5itV3v2z0qv8A06V9C4ug0jy0E',
    ))
    # await sqlx.insert(User).values(username='initial', password='password').returning('username').one()
    await sqlx.update(User).set(username='updated').where(
        sqlx.where(username='initial')
        and (
            sqlx.where(username='initial')
            or
            sqlx.where(password='password')
        )
    ).one()
    # await sqlx('SELECT * FROM user;').all()
    # users = tuple(user async for user in sqlx.select(User))
    # await sqlx.delete(User).where(username='updated').returning(User.username).all()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
