import os
import pyodbc
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create and return a connection to the database"""
    connection_string = (
        f"Driver={os.getenv('DB_DRIVER')};"
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
        f"Uid={os.getenv('DB_USER')};"
        f"Pwd={os.getenv('DB_PASSWORD')};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    
    return pyodbc.connect(connection_string)

def execute_query(query, params=None, fetch=True):
    """Execute a query and return results if needed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()