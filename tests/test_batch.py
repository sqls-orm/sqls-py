import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_batch_direct(sqlx: SQLX) -> None:
    async with sqlx as cnn:
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
async def test_batch_indirect(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        users = await cnn.insert(User).values(username='u', password='p')
        print(users)
        users = await cnn.insert(User).values(username='u', password='p')
        print(users)
