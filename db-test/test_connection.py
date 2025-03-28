import pyodbc
import sys

def test_connection():
    # Connection string
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:bagel-tracker-dbserver.database.windows.net,1433;"
        "Database=bagel-tracker-db;"
        "Uid=yuhang;"
        "Pwd=qq978962837Q;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    try:
        # Establish connection
        print("Attempting to connect to the database...")
        conn = pyodbc.connect(connection_string)
        
        # Create a cursor
        cursor = conn.cursor()
        
        # Execute a simple query
        print("Connection successful! Executing test query...")
        cursor.execute("SELECT @@VERSION")
        
        # Fetch and print the result
        row = cursor.fetchone()
        print(f"SQL Server version: {row[0]}")
        
        # Close the cursor and connection
        cursor.close()
        conn.close()
        print("Connection test completed successfully!")
        
    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()