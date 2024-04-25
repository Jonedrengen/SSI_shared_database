from Database_Connection import get_db_connection_string
from sqlalchemy import create_engine

def connect_to_database():
    conn_str = get_db_connection_string()
    try:
        engine = create_engine(conn_str)
        conn = engine.connect()
    except Exception as e:
        conn = None
        print(e)
    print(conn)
    return conn

connect_to_database()