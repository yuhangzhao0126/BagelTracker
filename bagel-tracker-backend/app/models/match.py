from app.utils.db import execute_query, get_db_connection
import pyodbc
from datetime import datetime

class Match:
    def __init__(self, match_id=None, match_type=None, match_date=None, 
                 reporter_user_id=None, team1_player1_id=None, team1_player2_id=None,
                 team2_player1_id=None, team2_player2_id=None, team1_score=None,
                 team2_score=None, winner_team=None, is_bagel=None,
                 created_at=None, updated_at=None):
        self.match_id = match_id
        self.match_type = match_type
        self.match_date = match_date or datetime.now()
        self.reporter_user_id = reporter_user_id
        self.team1_player1_id = team1_player1_id
        self.team1_player2_id = team1_player2_id
        self.team2_player1_id = team2_player1_id
        self.team2_player2_id = team2_player2_id
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.winner_team = winner_team
        self.is_bagel = is_bagel
        self.created_at = created_at
        self.updated_at = updated_at
    
    @staticmethod
    def find_by_id(match_id):
        """Find a match by ID."""
        query = "SELECT * FROM Matches WHERE match_id = ?"
        result = execute_query(query, (match_id,))
        if result:
            match_data = result[0]
            return Match(
                match_id=match_data.match_id,
                match_type=match_data.match_type,
                match_date=match_data.match_date,
                reporter_user_id=match_data.reporter_user_id,
                team1_player1_id=match_data.team1_player1_id,
                team1_player2_id=match_data.team1_player2_id,
                team2_player1_id=match_data.team2_player1_id,
                team2_player2_id=match_data.team2_player2_id,
                team1_score=match_data.team1_score,
                team2_score=match_data.team2_score,
                winner_team=match_data.winner_team,
                is_bagel=match_data.is_bagel,
                created_at=match_data.created_at,
                updated_at=match_data.updated_at
            )
        return None
    
    @staticmethod
    def get_matches_by_user(user_id, limit=10):
        """Get matches where user is a player, ordered by most recent."""
        query = """
            SELECT TOP ? * FROM Matches 
            WHERE team1_player1_id = ? 
               OR team1_player2_id = ? 
               OR team2_player1_id = ? 
               OR team2_player2_id = ? 
            ORDER BY match_date DESC
        """
        result = execute_query(query, (limit, user_id, user_id, user_id, user_id))
        return [
            {
                "match_id": row.match_id,
                "match_type": row.match_type,
                "match_date": str(row.match_date),
                "team1_player1_id": row.team1_player1_id,
                "team1_player2_id": row.team1_player2_id,
                "team2_player1_id": row.team2_player1_id,
                "team2_player2_id": row.team2_player2_id,
                "team1_score": row.team1_score,
                "team2_score": row.team2_score,
                "winner_team": row.winner_team,
                "is_bagel": row.is_bagel,
                "created_at": str(row.created_at)
            }
            for row in result
        ]
    
    @staticmethod
    def get_all_matches(limit=50):
        """Get all matches, ordered by most recent."""
        query = f"""
            SELECT TOP {limit} * FROM Matches 
            ORDER BY match_date DESC
        """
        result = execute_query(query)
        return [
            {
                "match_id": row.match_id,
                "match_type": row.match_type,
                "match_date": str(row.match_date),
                "reporter_user_id": row.reporter_user_id,
                "team1_player1_id": row.team1_player1_id,
                "team1_player2_id": row.team1_player2_id,
                "team2_player1_id": row.team2_player1_id,
                "team2_player2_id": row.team2_player2_id,
                "team1_score": row.team1_score,
                "team2_score": row.team2_score,
                "winner_team": row.winner_team,
                "is_bagel": row.is_bagel,
                "created_at": str(row.created_at)
            }
            for row in result
        ]
    
    def calculate_winner_and_bagel(self):
        """Calculate the winner team and whether the match was a bagel."""
        if self.team1_score > self.team2_score:
            self.winner_team = 1
        elif self.team2_score > self.team1_score:
            self.winner_team = 2
        else:
            self.winner_team = None  # Tie or not set
        
        # A match is a "bagel" if one team scores 6 and the other scores 0
        self.is_bagel = (self.team1_score == 6 and self.team2_score == 0) or \
                        (self.team1_score == 0 and self.team2_score == 6)
    
    def save(self):
        """Save match to database."""
        # Calculate winner and bagel status before saving
        self.calculate_winner_and_bagel()
        
        if self.match_id:
            # Update existing match
            query = """
                UPDATE Matches 
                SET match_type = ?, match_date = ?, reporter_user_id = ?,
                    team1_player1_id = ?, team1_player2_id = ?, 
                    team2_player1_id = ?, team2_player2_id = ?,
                    team1_score = ?, team2_score = ?, 
                    winner_team = ?, is_bagel = ?, updated_at = GETDATE()
                WHERE match_id = ?
            """
            execute_query(query, (
                self.match_type, self.match_date, self.reporter_user_id,
                self.team1_player1_id, self.team1_player2_id,
                self.team2_player1_id, self.team2_player2_id,
                self.team1_score, self.team2_score,
                self.winner_team, self.is_bagel, self.match_id
            ), fetch=False)
        else:
            # Insert new match
            conn = get_db_connection()
            cursor = conn.cursor()
            
            try:
                # Insert the match
                insert_query = """
                    INSERT INTO Matches (
                        match_type, match_date, reporter_user_id,
                        team1_player1_id, team1_player2_id, 
                        team2_player1_id, team2_player2_id,
                        team1_score, team2_score, winner_team, is_bagel
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(insert_query, (
                    self.match_type, self.match_date, self.reporter_user_id,
                    self.team1_player1_id, self.team1_player2_id,
                    self.team2_player1_id, self.team2_player2_id,
                    self.team1_score, self.team2_score,
                    self.winner_team, self.is_bagel
                ))
                
                # Get the ID
                cursor.execute("SELECT SCOPE_IDENTITY() AS match_id")
                result = cursor.fetchone()
                self.match_id = result.match_id
                
                conn.commit()
            except pyodbc.IntegrityError as e:
                conn.rollback()
                error_msg = str(e)
                if "FOREIGN KEY constraint" in error_msg:
                    raise ValueError("One or more players do not exist in the system")
                raise e
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        
        return self