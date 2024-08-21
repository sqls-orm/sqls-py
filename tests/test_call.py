import pytest

from sqlx import SQLX


@pytest.mark.asyncio(scope='session')
async def test_call_insert_default(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        users = await cnn(
            'INSERT INTO `user` (username, password) VALUES (%s, %s)',
            ('username', 'password'),
        )
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_call_select_one(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        user = await cnn(
            'SELECT `password` FROM `user` WHERE `username` = %s',
            ('username',),
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_call_update_default(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        await cnn(
            'UPDATE `user` SET `password` = %s WHERE `username` = %s',
            ('updated', 'username'),
        )


@pytest.mark.asyncio(scope='session')
async def test_call_select_aiter(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        async for user in cnn('SELECT * FROM `user`'):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_call_select_all(sqlx: SQLX) -> None:
    async with sqlx as cnn:
        for user in await cnn('SELECT * FROM `user`').all():
            print(user)
