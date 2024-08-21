import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_delete_all(sqlx: SQLX):
    async with sqlx as cnn:
        users = await cnn.delete(User).all()
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_delete_one(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.delete(User).first()
        print(user)
