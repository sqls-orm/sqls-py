from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    # 1. args
    async with sqlx as cnn:
        async for user in cnn.select(User.model().username, User.model().password).fr0m(User):
            print(user)

    # 1. kwargs
    async with sqlx as cnn:
        async for user in cnn.select(username=User.model().username, password=User.model().password).fr0m(User):
            print(user)

    # 1. args + kwargs
    async with sqlx as cnn:
        async for user in cnn.select(User.model().username, password=User.model().password).fr0m(User):
            print(user)
