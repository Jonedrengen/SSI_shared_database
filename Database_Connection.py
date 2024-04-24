import pyodbc
import csv

# get db connection string
def get_db_connection_string():
    # Set up the connection string
    server = 'localhost'
    database = 'SharedDatabase'
    username = 'sa'
    password = 'BlueBox21'
    conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    return conn_str

#connect to the db
def connect_to_database():
    conn_str = get_db_connection_string()
    try:
        conn = pyodbc.connect(conn_str)
    except pyodbc.Error as e:
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