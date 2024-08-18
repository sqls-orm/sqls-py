import aiomysql

from sqlx import SQLX


async def db():
    return SQLX(pool=await aiomysql.create_pool(
        db='temp',
        user='admin',
        password='n1AIRSaPV8EDx5itV3v2z0qv8A06V9C4ug0jy0E',
    ))
