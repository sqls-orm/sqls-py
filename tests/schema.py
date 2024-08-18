from pydantic import Field

from sqlx import Schema


class User(Schema):
    __table__ = 'user'

    username: str = Field()
    password: str = Field()
