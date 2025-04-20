from app.utils.db import execute_query
from passlib.hash import pbkdf2_sha256
from app.utils.db import get_db_connection
import pyodbc

class User:
    def __init__(self, user_id=None, name=None, email=None, password_hash=None, 
                 created_at=None, updated_at=None, is_active=True):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
    
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against a provided password."""
        return pbkdf2_sha256.verify(provided_password, stored_password)
    
    @staticmethod
    def find_by_email(email):
        """Find a user by email."""
        query = "SELECT * FROM Users WHERE email = ?"
        result = execute_query(query, (email,))
        if result:
            user_data = result[0]
            return User(
                user_id=user_data.user_id,
                name=user_data.name,
                email=user_data.email,
                password_hash=user_data.password_hash,
                created_at=user_data.created_at,
                updated_at=user_data.updated_at,
                is_active=user_data.is_active
            )
        return None
    
    @staticmethod
    def find_by_name(name):
        """Find a user by name."""
        query = "SELECT * FROM Users WHERE name = ?"
        result = execute_query(query, (name,))
        if result:
            user_data = result[0]
            return User(
                user_id=user_data.user_id,
                name=user_data.name,
                email=user_data.email,
                password_hash=user_data.password_hash,
                created_at=user_data.created_at,
                updated_at=user_data.updated_at,
                is_active=user_data.is_active
            )
        return None
    
    @staticmethod
    def search_users_by_prefix(prefix):
        """Search for users whose name starts with the given prefix.
        Returns a maximum of 5 results.
        """
        query = """
            SELECT TOP 5 user_id, name, email, created_at, is_active 
            FROM Users 
            WHERE name LIKE ?
            ORDER BY name
        """
        search_param = f"{prefix}%"  # Add wildcard to search by prefix
        result = execute_query(query, (search_param,))
        return [
            {
                "user_id": row.user_id,
                "name": row.name,
                "email": row.email,
                "created_at": str(row.created_at),
                "is_active": row.is_active
            }
            for row in result
        ]
    
    @staticmethod
    def get_all_users():
        """Get all users from the database."""
        query = """
            SELECT user_id, name, email, created_at, is_active 
            FROM Users
            ORDER BY name
        """
        result = execute_query(query)
        return [
            {
                "user_id": row.user_id,
                "name": row.name,
                "email": row.email,
                "created_at": str(row.created_at),
                "is_active": row.is_active
            }
            for row in result
        ]
    
    def save(self):
        """Save user to database."""
        if self.user_id:
            # Update existing user
            query = """
                UPDATE Users 
                SET name = ?, email = ?, password_hash = ?, 
                    updated_at = GETDATE(), is_active = ?
                WHERE user_id = ?
            """
            execute_query(query, (
                self.name, self.email, self.password_hash,
                self.is_active, self.user_id
            ), fetch=False)
        else:
            # Insert new user
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                # First, insert the user
                insert_query = """
                    INSERT INTO Users (name, email, password_hash)
                    VALUES (?, ?, ?)
                """
                cursor.execute(insert_query, (
                    self.name, self.email, self.password_hash
                ))
                
                # Then get the ID
                cursor.execute("SELECT SCOPE_IDENTITY() AS user_id")
                result = cursor.fetchone()
                self.user_id = result.user_id
                
                conn.commit()
            except pyodbc.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                if "Violation of UNIQUE KEY constraint" in error_msg:
                    if "idx_users_email" in error_msg:
                        raise ValueError("Email address is already registered")
                    elif "idx_users_name" in error_msg:
                        raise ValueError("Username is already taken")
                    else:
                        raise ValueError("A user with this information already exists")
                raise e
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        
        return self