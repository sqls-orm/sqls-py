from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    async with sqlx as cnn:
        users = await cnn('SELECT * FROM user').all()
        print(users)
