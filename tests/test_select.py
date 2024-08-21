import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_select_args(sqlx: SQLX):
    async with sqlx as cnn:
        async for user in cnn.select(
                User.model().username,
                User.model().password,
        ).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_kwargs(sqlx: SQLX):
    async with sqlx as cnn:
        async for user in cnn.select(
                username=User.model().username,
                password=User.model().password,
        ).fr0m(User):
            print(user)

    async with sqlx as cnn:
        async for user in cnn.select(**{
            'username': User.model().username,
            'password': User.model().password,
        }).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_alias(sqlx: SQLX):
    async with sqlx as cnn:
        async for user in cnn.select({
            'username': User.model().username,
            'password': User.model().password,
        }).fr0m(User):
            print(user)


@pytest.mark.asyncio(scope='session')
async def test_select_mixed(sqlx: SQLX):
    async with sqlx as cnn:
        async for user in cnn.select(
                User.model().id,
                name='username',
                password=User.model().password,
        ).fr0m(User):
            print(user)
