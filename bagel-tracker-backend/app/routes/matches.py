from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.match_service import MatchService
from app.models.user import User
import json

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('', methods=['POST'])
@jwt_required()
def record_match():
    """Record a new tennis match."""
    # Get current user from JWT
    current_user_json = get_jwt_identity()
    try:
        current_user = json.loads(current_user_json)
        reporter_user_id = current_user.get('user_id')
    except:
        return jsonify({"success": False, "message": "Invalid user identity in token"}), 400
    
    # Get match data from request
    match_data = request.get_json()
    if not match_data:
        return jsonify({"success": False, "message": "No match data provided"}), 400
    
    # Handle username to user_id conversion for player fields
    username_fields = {
        'team1_player1_name': 'team1_player1_id',
        'team1_player2_name': 'team1_player2_id',
        'team2_player1_name': 'team2_player1_id',
        'team2_player2_name': 'team2_player2_id'
    }
    
    # Convert usernames to user IDs if usernames are provided
    for name_field, id_field in username_fields.items():
        if name_field in match_data and match_data[name_field]:
            username = match_data[name_field]
            user = User.find_by_name(username)
            if not user:
                return jsonify({"success": False, "message": f"User not found: {username}"}), 400
            
            # Add the user ID to match data
            match_data[id_field] = user.user_id
    
    # Process integers for player IDs and scores
    for field in ['team1_player1_id', 'team1_player2_id', 'team2_player1_id', 
                  'team2_player2_id', 'team1_score', 'team2_score']:
        if field in match_data and match_data[field] is not None:
            try:
                match_data[field] = int(match_data[field])
            except (ValueError, TypeError):
                if field.endswith('score'):
                    return jsonify({"success": False, "message": f"{field} must be an integer"}), 400
    
    # Call service to record match
    result = MatchService.record_match(reporter_user_id, match_data)
    
    if result["success"]:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@matches_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_matches(user_id):
    """Get matches for a specific user."""
    # Get limit parameter from query string (default to 10)
    try:
        limit = int(request.args.get('limit', 10))
    except ValueError:
        limit = 10
    
    # Call service to get matches
    result = MatchService.get_user_matches(user_id, limit)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@matches_bp.route('/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match(match_id):
    """Get a specific match by ID."""
    from app.models.match import Match
    
    match = Match.find_by_id(match_id)
    if match:
        match_data = {
            "match_id": match.match_id,
            "match_type": match.match_type,
            "match_date": str(match.match_date),
            "reporter_user_id": match.reporter_user_id,
            "team1_player1_id": match.team1_player1_id,
            "team1_player2_id": match.team1_player2_id,
            "team2_player1_id": match.team2_player1_id,
            "team2_player2_id": match.team2_player2_id,
            "team1_score": match.team1_score,
            "team2_score": match.team2_score,
            "winner_team": match.winner_team,
            "is_bagel": match.is_bagel,
            "created_at": str(match.created_at)
        }
        return jsonify({"success": True, "match": match_data}), 200
    else:
        return jsonify({"success": False, "message": "Match not found"}), 404

@matches_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_matches():
    """Get all tennis matches from the database."""
    try:
        # Get limit parameter from query string (default to 50)
        limit = int(request.args.get('limit', 50))
    except ValueError:
        limit = 50
    
    # Call service to get all matches
    result = MatchService.get_all_matches(limit)
    
    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 500