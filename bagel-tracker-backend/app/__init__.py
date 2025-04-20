from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # 1 hour
    
    # Initialize extensions
    CORS(app, origins=["https://icy-mushroom-0938c2500.6.azurestaticapps.net", "http://localhost:3000", "http://localhost:3001"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    JWTManager(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Register matches blueprint
    from app.routes.matches import matches_bp
    app.register_blueprint(matches_bp, url_prefix='/api/matches')
    
    # Register ping blueprint
    from app.routes.ping import ping_bp
    app.register_blueprint(ping_bp, url_prefix='/api/ping')
    
    return app
