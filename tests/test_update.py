import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_update_kwargs(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        )
        print(user)
