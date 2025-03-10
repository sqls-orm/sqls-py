import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_batch_direct(sqls: SQLS) -> None:
    async with sqls as cnn:
        users = await cnn(
            'INSERT INTO `user` (username, password) VALUES (%s, %s)',
            ('username', 'password'),
        )
        print(users)
        users = await cnn(
            'INSERT INTO `user` (username, password) VALUES (%s, %s)',
            ('username', 'password'),
        )
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_batch_indirect(sqls: SQLS) -> None:
    async with sqls as cnn:
        users = await cnn.insert(User).values(username='u', password='p')
        print(users)
        users = await cnn.insert(User).values(username='u', password='p')
        print(users)
