import pyodbc
import csv

# REPLACE DB CONNECTION STRING IN DATABASE_CONNECTION. IF YOU WANT TO INSERT CSV FILES INTO THE DATABASE
# THE ONE IN DATABASE_CONNECTION WORKS FOR APIS

def connect_to_db():
    # Set up the connection string
    server = 'localhost'
    database = 'SharedDatabase'
    username = 'sa'
    password = 'BlueBox21'
    driver = '{ODBC Driver 18 for SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'

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