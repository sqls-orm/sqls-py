from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    # 1. one | kwargs | Schema
    async with sqlx as cnn:
        user = await cnn.insert(User).values(
            username='username',
            password='password',
        ).returning(
            username=User.model().username,
            password=User.model().password,
        ).one()
        print(user)

    # 2. one | Schema | args
    async with sqlx as cnn:
        user = await cnn.insert(User).values({
            User.model().username: 'username',
            User.model().password: 'password',
        }).returning(
            'username',
            'password',
        ).one()
        print(user)

    # 3. many | list[dict] | Schema
    async with sqlx as cnn:
        users = await cnn.insert(User).values([
            dict(
                username='username',
                password='password',
            ),
            dict(
                username='username',
                password='password',
            )
        ]).returning(
            username=User.model().username,
            password=User.model().password,
        ).all()
        print(users)

    # 4. many | list[Schema] | args
    async with sqlx as cnn:
        users = await cnn.insert(User).values([
            {
                User.model().username: 'username',
                User.model().password: 'password',
            },
            {
                User.model().username: 'username',
                User.model().password: 'password',
            }
        ]).returning('username', 'password').one()
        print(users)
