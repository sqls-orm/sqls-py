import aiomysql
import pytest_asyncio as aiopytest
from pydantic import Field

from sqls import SQLS, Schema


@aiopytest.fixture(scope='session')
async def sqls():
    _sqls = SQLS(
        db='test',
        user='root',
        password='password',
    )
    async with _sqls as _cnn:
        await _cnn('''
            CREATE TABLE IF NOT EXISTS `user` (
              `id` int(11) PRIMARY KEY AUTO_INCREMENT,
              `username` text NOT NULL,
              `password` text NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        ''').execute()

    yield _sqls


class User(Schema):
    __table__ = 'user'

    id: int = Field()
    username: str = Field()
    password: str = Field()
