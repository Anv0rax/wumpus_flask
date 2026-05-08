import psycopg
from psycopg.rows import dict_row
from private import *

def get_connection():
    return psycopg.connect(
        host = DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        row_factory = dict_row
    )

print(get_connection())