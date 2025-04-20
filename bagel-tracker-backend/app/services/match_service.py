from app.models.match import Match
from app.models.user import User

class MatchService:
    @staticmethod
    def record_match(reporter_user_id, match_data):
        """
        Records a new tennis match.
        
        Args:
            reporter_user_id (int): The user ID of the person reporting the match
            match_data (dict): Data for the match (match_type, player names/IDs, scores)
            
        Returns:
            dict: Result of the operation with success status, message, and match_id if successful
        """
        try:
            # Convert player names to IDs if names are provided
            name_to_id_mapping = {
                'team1_player1_name': 'team1_player1_id',
                'team1_player2_name': 'team1_player2_id',
                'team2_player1_name': 'team2_player1_id',
                'team2_player2_name': 'team2_player2_id'
            }
            
            for name_field, id_field in name_to_id_mapping.items():
                if name_field in match_data and match_data[name_field]:
                    username = match_data[name_field]
                    user = User.find_by_name(username)
                    if not user:
                        return {
                            "success": False,
                            "message": f"User not found: {username}"
                        }
                    match_data[id_field] = user.user_id
            
            # Validate required fields - now checking for IDs that may have been converted from names
            required_fields = ['match_type', 'team1_player1_id', 'team2_player1_id', 
                              'team1_score', 'team2_score']
            
            for field in required_fields:
                if field not in match_data or match_data[field] is None:
                    return {
                        "success": False, 
                        "message": f"Missing required field: {field}"
                    }
            
            # Validate match type
            match_type = match_data['match_type']
            if match_type not in ['singles', 'doubles']:
                return {
                    "success": False,
                    "message": "Invalid match type. Must be 'singles' or 'doubles'"
                }
            
            # Validate players
            team1_player1_id = match_data['team1_player1_id']
            team2_player1_id = match_data['team2_player1_id']
            team1_player2_id = match_data.get('team1_player2_id')
            team2_player2_id = match_data.get('team2_player2_id')
            
            # Check if all specified players exist
            player_ids = [team1_player1_id, team2_player1_id]
            if match_type == 'doubles':
                if team1_player2_id is None or team2_player2_id is None:
                    return {
                        "success": False,
                        "message": "Doubles match requires four players"
                    }
                player_ids.extend([team1_player2_id, team2_player2_id])
            
            # Validate no player is listed twice
            if len(set(player_ids)) < len(player_ids):
                return {
                    "success": False,
                    "message": "A player cannot be listed more than once in a match"
                }
            
            # Validate scores (must be non-negative integers)
            team1_score = match_data['team1_score']
            team2_score = match_data['team2_score']
            
            if not isinstance(team1_score, int) or not isinstance(team2_score, int):
                return {
                    "success": False,
                    "message": "Scores must be integers"
                }
            
            if team1_score < 0 or team2_score < 0:
                return {
                    "success": False,
                    "message": "Scores cannot be negative"
                }
            
            # Validate at least one team has a valid tennis score (usually 6 for a standard set)
            if max(team1_score, team2_score) < 6:
                return {
                    "success": False,
                    "message": "At least one team should have a score of 6 or higher for a completed match"
                }
            
            # Create and save the match
            match = Match(
                match_type=match_type,
                reporter_user_id=reporter_user_id,
                team1_player1_id=team1_player1_id,
                team1_player2_id=team1_player2_id,
                team2_player1_id=team2_player1_id,
                team2_player2_id=team2_player2_id,
                team1_score=team1_score,
                team2_score=team2_score
            )
            
            # Save will calculate winner and bagel status
            match.save()
            
            return {
                "success": True,
                "message": "Match recorded successfully",
                "match_id": match.match_id,
                "is_bagel": match.is_bagel
            }
            
        except ValueError as e:
            return {"success": False, "message": str(e)}
        except Exception as e:
            return {"success": False, "message": f"Error recording match: {str(e)}"}
            
    @staticmethod
    def get_user_matches(user_id, limit=10):
        """
        Get recent matches for a specific user.
        
        Args:
            user_id (int): The user ID to fetch matches for
            limit (int): Maximum number of matches to return
            
        Returns:
            dict: Result with matches list and success status
        """
        try:
            matches = Match.get_matches_by_user(user_id, limit)
            return {
                "success": True,
                "message": "Matches retrieved successfully",
                "matches": matches
            }
        except Exception as e:
            return {"success": False, "message": f"Error retrieving matches: {str(e)}"}
    
    @staticmethod
    def get_all_matches(limit=50):
        """
        Get all matches from the database, with an optional limit.
        
        Args:
            limit (int): Maximum number of matches to return
            
        Returns:
            dict: Result with matches list and success status
        """
        try:
            # Call the static method on Match model
            matches = Match.get_all_matches(limit)
            return {
                "success": True,
                "message": "Matches retrieved successfully",
                "matches": matches
            }
        except Exception as e:
            return {"success": False, "message": f"Error retrieving matches: {str(e)}"}