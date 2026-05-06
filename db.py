from dotenv import load_dotenv
load_dotenv()
import os
import psycopg
from psycopg.rows import dict_row

def get_connection():
    return psycopg.connect(
        host = os.environ['DB_HOST'],
        port = int(os.environ.get("DB_PORT", "5433")),
        dbname = os.environ['DB_NAME'],
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        row_factory = dict_row
    )

print(get_connection())

