from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    async with sqlx as cnn:
        users = await cnn.delete(User).where({
            User.model().username: 'username',
        }).returning(User.username).all()
        print(users)
