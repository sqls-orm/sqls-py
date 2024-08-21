import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_whereand_kwargs(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where_and(
            username='initial',
            password='password',
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_whereand_schema(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where_and({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_whereand_column(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where_and(
            (User.model().username == 'initial') | (User.model().password == 'password')
        ).first()
        print(user)
