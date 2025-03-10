import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_whereor_kwargs(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where_or(
            username='initial',
            password='password',
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_whereor_schema(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where_or({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_whereor_column(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where_or(
            (User.model().username == 'initial') | (User.model().password == 'password')
        ).first()
        print(user)
