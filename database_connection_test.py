import pyodbc
import csv

def connect_to_db():
    # Set up the connection string
    server = 'localhost'
    database = 'SharedDatabase'
    username = 'sa'
    password = 'BlueBox21'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Connect to the database
    try:
        conn = pyodbc.connect(conn_str)
        print("Connection successful")
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Failed to connect to the database. SQLSTATE: {sqlstate}")
        conn = None
    print(conn)
    return conn

connect_to_db()