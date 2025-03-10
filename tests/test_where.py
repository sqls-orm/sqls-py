import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_column_simple(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where(
            User.model().username == 'initial'
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_simple_and(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where(
            (User.model().username == 'initial')
            &
            (User.model().password == 'password')
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_simple_or(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where(
            (User.model().username == 'initial')
            |
            (User.model().password == 'password')
        ).all()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_complex(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.select().fr0m(User).where(
            ((User.model().username == 'username') & (User.model().password == 'updated'))
            |
            ((User.model().username == 'initial') & (User.model().password == 'password'))
        ).all()
        print(user)
