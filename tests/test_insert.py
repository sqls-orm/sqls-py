import pytest

from sqlx import SQLX
from .conftest import User


@pytest.mark.asyncio(scope='session')
async def test_insert_kwargs_kwargs_one(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.insert().into(User).values(
            username='username',
            password='password',
        )
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_insert_schema_args_one(sqlx: SQLX):
    async with sqlx as cnn:
        user = await cnn.insert().into(User).values({
            User.model().username: 'username',
            User.model().password: 'password',
        })
        print(user)


@pytest.mark.asyncio(scope='session')
async def test_insert_kwargs_kwargs_many(sqlx: SQLX):
    async with sqlx as cnn:
        users = await cnn.insert().into(User).values([
            dict(
                username='username',
                password='password',
            ),
            dict(
                username='username',
                password='password',
            )
        ])
        print(users)


@pytest.mark.asyncio(scope='session')
async def test_insert_schema_args_many(sqlx: SQLX):
    async with sqlx as cnn:
        users = await cnn.insert().into(User).values([
            {
                User.model().username: 'username',
                User.model().password: 'password',
            },
            {
                User.model().username: 'username',
                User.model().password: 'password',
            }
        ])
        print(users)
