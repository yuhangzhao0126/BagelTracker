from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

ping_bp = Blueprint('ping', __name__)

@ping_bp.route('', methods=['GET'])
@jwt_required()
def ping_endpoint():
    """
    A simple endpoint that does nothing but verify that the user is authenticated.
    Requires a valid JWT token.
    """
    # Get the identity of the current user from the JWT
    # Since we're storing the identity as a JSON string, we need to parse it
    current_user_json = get_jwt_identity()
    try:
        current_user = json.loads(current_user_json)
    except:
        current_user = {"error": "Could not parse user identity"}
    
    return jsonify({
        "success": True,
        "message": "Authentication successful",
        "user": current_user
    }), 200