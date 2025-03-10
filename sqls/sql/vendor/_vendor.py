import aiomysql


class VendorBase:
    pool: aiomysql.Pool
