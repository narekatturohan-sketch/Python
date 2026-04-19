import oracledb

pool = None

def init_db_pool():
    global pool 
    pool = oracledb.create_pool(
        user="PRODN",
        password="Prodn0123#",
        dsn="localhost:1521/FREEPDB1",
        min=2,
        max=5,
        increment=1
    )

def get_db_connection():
    if pool is None:
        init_db_pool()
    return pool.acquire()