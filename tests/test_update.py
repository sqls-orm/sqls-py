import pytest

from sqls import SQLS
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_update_kwargs(sqls: SQLS):
    async with sqls as cnn:
        user = await cnn.update(User).set(
            username='initial',
        )
        print(user)
