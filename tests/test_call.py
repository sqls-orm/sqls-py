import pytest

from sqls import SQLS


@pytest.mark.asyncio(scope='session')
async def test_call_insert_default(sqls: SQLS) -> None:
    async with sqls as cnn:
        users = await cnn(
            'INSERT INTO `user` (username, password) VALUES (%s, %s)',
            ('username', 'password'),
        )
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_call_select_one(sqls: SQLS) -> None:
    async with sqls as cnn:
        user = await cnn(
            'SELECT `password` FROM `user` WHERE `username` = %s',
            ('username',),
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_call_update_default(sqls: SQLS) -> None:
    async with sqls as cnn:
        await cnn(
            'UPDATE `user` SET `password` = %s WHERE `username` = %s',
            ('updated', 'username'),
        )


@pytest.mark.asyncio(scope='session')
async def test_call_select_aiter(sqls: SQLS) -> None:
    async with sqls as cnn:
        async for user in cnn('SELECT * FROM `user`'):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_call_select_all(sqls: SQLS) -> None:
    async with sqls as cnn:
        for user in await cnn('SELECT * FROM `user`').all():
            print(user)
