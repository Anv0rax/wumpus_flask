import psycopg
from psycopg.rows import dict_row
from private import *
from flask import session

def get_connection():
    return psycopg.connect(
        host = DB_HOST,
        port = DB_PORT,
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        row_factory = dict_row
    )

def add_info_in_db(result_code):
    if 'username' not in session :
        return

    column_map = {
        -1: "numberofvictories",
        -2: "defeats",
        -3: "fell_slime_pit",
        -4: "missed",
        3: "bat_touched"
    }

    column_to_update = column_map.get(result_code)

    if not column_to_update:
        return

    points = 0
    if result_code == -1:
        points = (session.get('difficulty', 0) + 1) * 10

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = f"""UPDATE user_table SET {column_to_update} = {column_to_update} + 1, score = score + %s WHERE username = %s"""
                cursor.execute(query, (points, session['username']))
                conn.commit()
    except Exception as e:
        print(f"Error, couldn't register the new value of the score : {e}")