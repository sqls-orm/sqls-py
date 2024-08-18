from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    async with sqlx as cnn:
        user = await cnn.insert(User).values(
            username='username',
            password='password',
        ).returning(
            username=User.model().username,
            password=User.model().password,
        ).one()
        print(user)

    async with sqlx as cnn:
        user = await cnn.insert(User).values({
            User.model().username: 'username',
            User.model().password: 'password',
        }).returning(
            username=User.model().username,
            password=User.model().password,
        ).one()
        print(user)

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
        ]).returning(
            username=User.model().username,
            password=User.model().password,
        ).one()
        print(users)

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
        ).one()
        print(users)
