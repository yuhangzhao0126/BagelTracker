from app.utils.db import execute_query
from passlib.hash import pbkdf2_sha256
from app.utils.db import get_db_connection

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
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        
        return self