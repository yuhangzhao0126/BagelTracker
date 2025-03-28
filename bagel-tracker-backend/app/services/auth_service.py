from app.models.user import User
from flask_jwt_extended import create_access_token
import datetime

class AuthService:
    @staticmethod
    def register_user(name, email, password):
        """Register a new user."""
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return {"success": False, "message": "Email already registered"}
        
        # Create new user
        password_hash = User.hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )
        
        # Save user to database
        try:
            new_user.save()
            
            # Generate JWT token
            token = create_access_token(
                identity={"user_id": new_user.user_id, "email": email},
                expires_delta=datetime.timedelta(hours=1)
            )
            
            return {
                "success": True,
                "message": "User registered successfully",
                "token": token,
                "user": {
                    "user_id": new_user.user_id,
                    "name": name,
                    "email": email
                }
            }
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
            
    @staticmethod
    def login_user(email, password):
        """Login a user."""
        user = User.find_by_email(email)
        
        if not user or not User.verify_password(user.password_hash, password):
            return {"success": False, "message": "Invalid email or password"}
        
        # Generate JWT token
        token = create_access_token(
            identity={"user_id": user.user_id, "email": user.email},
            expires_delta=datetime.timedelta(hours=1)
        )
        
        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email
            }
        }