from app.utils.db import execute_query

def create_tables():
    """Create the necessary tables if they don't exist."""
    # Create Users table
    users_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
    CREATE TABLE Users (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        email NVARCHAR(100) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE(),
        is_active BIT DEFAULT 1
    );
    
    IF NOT EXISTS (SELECT * FROM sysindexes WHERE name='idx_users_email')
    CREATE INDEX idx_users_email ON Users(email);
    """
    
    # Execute query
    execute_query(users_table_query, fetch=False)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()