import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_select_args(sqls: SQLS):
    async with sqls as cnn:
        async for user in cnn.select(
                User.model().username,
                User.model().password,
        ).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_kwargs(sqls: SQLS):
    async with sqls as cnn:
        async for user in cnn.select(
                username=User.model().username,
                password=User.model().password,
        ).fr0m(User):
            print(user)

    async with sqls as cnn:
        async for user in cnn.select(**{
            'username': User.model().username,
            'password': User.model().password,
        }).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_alias(sqls: SQLS):
    async with sqls as cnn:
        async for user in cnn.select({
            'username': User.model().username,
            'password': User.model().password,
        }).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_mixed(sqls: SQLS):
    async with sqls as cnn:
        async for user in cnn.select(
                User.model().id,
                name='username',
                password=User.model().password,
        ).fr0m(User):
            print(user)
