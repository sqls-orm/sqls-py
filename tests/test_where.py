import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_column_simple(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where(
            User.model().username == 'initial'
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_simple_and(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where(
            (User.model().username == 'initial')
            &
            (User.model().password == 'password')
        ).first()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_simple_or(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where(
            (User.model().username == 'initial')
            |
            (User.model().password == 'password')
        ).all()
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_column_complex(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.select().fr0m(User).where(
            ((User.model().username == 'username') & (User.model().password == 'updated'))
            |
            ((User.model().username == 'initial') & (User.model().password == 'password'))
        ).all()
        print(user)
