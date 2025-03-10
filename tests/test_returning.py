import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_returning_kwargs(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.insert(User).values(
            username='username',
            password='password',
        ).returning(
            id=User.model().id,
            name=User.model().username,
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_returning_args(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.insert(User).values(
            username='username',
            password='password',
        ).returning(
            User.model().id,
            User.model().username,
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_returning_default(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.insert(User).values(
            username='username',
            password='password',
        ).returning().first()
        print(user)
