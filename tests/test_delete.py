import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_delete_all(sqls: SQLS):
    async with sqls as cnn:
        users = await cnn.delete(User).all()
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_delete_one(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.delete(User).first()
        print(user)
