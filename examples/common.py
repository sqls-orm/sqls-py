from sqlx import SQLX
import asyncio
import aiomysql


async def main():
    pool = await aiomysql.create_pool(
        db='test',
        user='root',
        password='password',
    )
    print(type(pool))
    async with pool as cnn:
        ...
    # pool = SQLX(
    #     db='test',
    #     user='root',
    #     password='password',
    # )
    # async with pool as cnn:
    #     ...
    # pool.close()
    # await pool.wait_closed()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
