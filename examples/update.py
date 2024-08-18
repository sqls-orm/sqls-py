from .sqlx import db
from .schema import User


async def test():
    sqlx = await db()

    # 1. where_and | kwargs | kwargs | one
    async with sqlx as cnn:
        cnn.update().where()
        user = await cnn.update(User).set(
            username='initial',
        ).where_and(
            username='initial',
            password='password',
        ).one()
        print(user)

    # 2. where_and | Schema | Schema | one
    async with sqlx as cnn:
        user = await cnn.update(User).set({
            User.model().username: 'initial',
        }).where_and({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).one()
        print(user)

    # 3. where_or | kwargs | kwargs | one
    async with sqlx as cnn:
        user = await cnn.update(User).set(
            username='initial',
        ).where_or(
            username='initial',
            password='password',
        ).one()
        print(user)

    # 4. where_or | Schema | Schema | one
    async with sqlx as cnn:
        user = await cnn.update(User).set({
            User.model().username: 'initial',
        }).where_or({
            User.model().username: 'initial',
            User.model().password: 'password',
        }).one()
        print(user)

    # 5. where | Schema | Column | one
    async with sqlx as cnn:
        user = await cnn.update(User).set({
            User.model().username: 'initial',
        }).where(
            (User.model().username == 'initial')
            &
            (User.model().password == 'password')
        ).one()
        print(user)

    # 6. where | Schema | Column | all
    async with sqlx as cnn:
        user = await cnn.update(User).set({
            User.model().username: 'initial',
        }).where(
            (User.model().username == 'initial')
            &
            (User.model().password == 'password')
        ).all()
        print(user)
