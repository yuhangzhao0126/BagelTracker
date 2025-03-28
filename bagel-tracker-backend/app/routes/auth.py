from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate input
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    # Register user
    result = AuthService.register_user(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password')
    )
    
    if result["success"]:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    data = request.get_json()
    
    # Validate input
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    # Login user
    result = AuthService.login_user(
        email=data.get('email'),
        password=data.get('password')
    )
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401