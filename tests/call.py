async def test():
    async with sqlx as cnn:
        users = await cnn('SELECT * FROM user').all()