import pyodbc
import csv
from sqlalchemy import create_engine

# THIS WAY OF USING CONNECTION STRING ONLY WORKS WHEN USING APIS, SO CHANGE TO THE CONNECTION STRING IN database_connection_for_csv_insertion.py
# WHEN YOU WANT TO 

# get db connection string
def get_db_connection_string():
    server = 'localhost'
    database = 'SharedDatabase'
    username = 'sa'
    password = 'BlueBox21'
    driver = 'ODBC Driver 18 for SQL Server'
    conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}&TrustServerCertificate=yes'
    return conn_str

#connect to the db
def connect_to_database():
    conn_str = get_db_connection_string()
    try:
        engine = create_engine(conn_str)
        conn = engine.connect()
        print("Connection successful")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        conn = None
    return conn

#execute a query
def execute_query(query, params=None): #params
    conn = connect_to_database()
    if conn is not None:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
        except pyodbc.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Cannot execute query. Connection to database failed.")

#insert a csv into mssql db
def insert_csv_to_db(csv_file_path, table_name):
    # Open your CSV file
    with open(csv_file_path, 'r') as f:
        # Parse the CSV file
        reader = csv.reader(f)
        columns = next(reader)  # Assuming the first row contains column names
        # Prepare the SQL query
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"
        # Insert each row
        for row in reader:
            execute_query(query, row)

#insert_csv_to_db('Patient_test_data.csv', 'SharedDatabase.dbo.Patient')