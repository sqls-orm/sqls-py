from pydantic import Field
from sqlx import SQLX, Schema
import asyncio


class User(Schema):
    __table__ = 'user'

    id: int = Field()
    username: str = Field()
    password: str = Field()


async def main():
    sqlx = SQLX(
        db='test',
        user='root',
        password='password',
    )

    await sqlx.create_pool()

    users = await sqlx.count().fr0m(User).where({
        User.model().username: 'username'
    }).order_by(
        User.model().username.desc()
    ).limit(10).offset(5).all()
    print(users)

    await sqlx.close_pool()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
