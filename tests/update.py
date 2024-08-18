from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    async with sqlx as cnn:
        user = await cnn.update(User).set({
            User.model().username: 'initial',
        }).where(
            (User.model().username == 'initial')
            &
            (User.model().password == 'password')
        ).one()
        print(user)

    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        ).where_and(
            username='initial',
            password='password',
        ).one()
        print(user)

    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        ).where_and({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).one()
        print(user)

    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        ).where_or(
            username='initial',
            password='password',
        ).one()
        print(user)

    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        ).where_or({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).one()
        print(user)
