from pydantic import Field

from sqlx import Schema


class User(Schema):
    __table__ = 'user'

    id: int = Field()
    username: str = Field()
    password: str = Field()
