yuhangzhao0126: Now let's add a feature to upload tennis match scores.
after user log in. The user can upload a tennis match score for both single(1 vs 1) and doubles(2 vs 2) match.
e.g.: user1 vs user2 results: 6:3.

Help me to design this feature. Let's start from backend.

GitHub Copilot: Okay, let's design the backend for the match score upload feature.

**1. Database Schema:**

We need a new table to store match results. Let's call it `Matches`.

*   **Table Name:** `Matches`
*   **Columns:**
    *   `match_id` (INT IDENTITY(1,1) PRIMARY KEY): Unique identifier for the match.
    *   `match_type` (NVARCHAR(10) NOT NULL): Type of match ('singles' or 'doubles'). Add a check constraint: `CHECK (match_type IN ('singles', 'doubles'))`.
    *   `match_date` (DATETIME DEFAULT GETDATE()): Date and time when the match was played (or recorded).
    *   `reporter_user_id` (INT NOT NULL): The ID of the user who reported the score. Foreign key referencing `Users(user_id)`.
    *   `team1_player1_id` (INT NOT NULL): User ID of the first player in team 1. Foreign key referencing `Users(user_id)`.
    *   `team1_player2_id` (INT NULL): User ID of the second player in team 1 (for doubles). Foreign key referencing `Users(user_id)`. Nullable.
    *   `team2_player1_id` (INT NOT NULL): User ID of the first player in team 2. Foreign key referencing `Users(user_id)`.
    *   `team2_player2_id` (INT NULL): User ID of the second player in team 2 (for doubles). Foreign key referencing `Users(user_id)`. Nullable.
    *   `team1_score` (INT NOT NULL): Score for team 1.
    *   `team2_score` (INT NOT NULL): Score for team 2.
    *   `winner_team` (INT NULL): Indicates the winning team (1 or 2). Can be calculated or stored. Let's plan to calculate and store it upon insertion.
    *   `is_bagel` (BIT DEFAULT 0): Flag indicating if the match was a bagel (e.g., 6-0 or 0-6). Calculated upon insertion.
    *   `created_at` (DATETIME DEFAULT GETDATE()): Timestamp of record creation.
    *   `updated_at` (DATETIME DEFAULT GETDATE()): Timestamp of last update.

**Action:** Update the database initialization script (`init_db.py`) to include the `CREATE TABLE` statement for `Matches`.

```python
from app.utils.db import execute_query

def create_tables():
    """Create the necessary tables if they don't exist."""
    # Create Users table
    users_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
    CREATE TABLE Users (
        user_id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL UNIQUE,
        email NVARCHAR(100) NOT NULL UNIQUE,
        password_hash NVARCHAR(255) NOT NULL,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE(),
        is_active BIT DEFAULT 1
    );
    
    IF NOT EXISTS (SELECT * FROM sysindexes WHERE name='idx_users_email')
    CREATE INDEX idx_users_email ON Users(email);
    
    IF NOT EXISTS (SELECT * FROM sysindexes WHERE name='idx_users_name')
    CREATE INDEX idx_users_name ON Users(name);
    """
    execute_query(users_table_query, fetch=False)
    
    # Create Matches table
    matches_table_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Matches' AND xtype='U')
    CREATE TABLE Matches (
        match_id INT IDENTITY(1,1) PRIMARY KEY,
        match_type NVARCHAR(10) NOT NULL CHECK (match_type IN ('singles', 'doubles')),
        match_date DATETIME DEFAULT GETDATE(),
        reporter_user_id INT NOT NULL,
        team1_player1_id INT NOT NULL,
        team1_player2_id INT NULL,
        team2_player1_id INT NOT NULL,
        team2_player2_id INT NULL,
        team1_score INT NOT NULL,
        team2_score INT NOT NULL,
        winner_team INT NULL,
        is_bagel BIT DEFAULT 0,
        created_at DATETIME DEFAULT GETDATE(),
        updated_at DATETIME DEFAULT GETDATE(),
        CONSTRAINT FK_Matches_Reporter FOREIGN KEY (reporter_user_id) REFERENCES Users(user_id),
        CONSTRAINT FK_Matches_T1P1 FOREIGN KEY (team1_player1_id) REFERENCES Users(user_id),
        CONSTRAINT FK_Matches_T1P2 FOREIGN KEY (team1_player2_id) REFERENCES Users(user_id),
        CONSTRAINT FK_Matches_T2P1 FOREIGN KEY (team2_player1_id) REFERENCES Users(user_id),
        CONSTRAINT FK_Matches_T2P2 FOREIGN KEY (team2_player2_id) REFERENCES Users(user_id)
    );

    IF NOT EXISTS (SELECT * FROM sysindexes WHERE name='idx_matches_reporter')
    CREATE INDEX idx_matches_reporter ON Matches(reporter_user_id);

    IF NOT EXISTS (SELECT * FROM sysindexes WHERE name='idx_matches_players')
    CREATE INDEX idx_matches_players ON Matches(team1_player1_id, team1_player2_id, team2_player1_id, team2_player2_id);
    """
    execute_query(matches_table_query, fetch=False)

    print("Database tables checked/created successfully!")

if __name__ == "__main__":
    create_tables()
```

**2. API Endpoint:**

*   **Route:** `POST /api/matches`
*   **Authentication:** Required (JWT)
*   **Request Body (JSON):**
    ```json
    {
      "match_type": "singles", // or "doubles"
      "team1_player1_id": 1,
      "team1_player2_id": null, // Required for doubles, null/absent for singles
      "team2_player1_id": 2,
      "team2_player2_id": null, // Required for doubles, null/absent for singles
      "team1_score": 6,
      "team2_score": 3
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
      "success": true,
      "message": "Match recorded successfully",
      "match_id": 123 // ID of the newly created match
    }
    ```
*   **Error Responses:**
    *   `400 Bad Request`: Invalid input (missing fields, invalid IDs, invalid scores, player conflicts, etc.)
    *   `401 Unauthorized`: Missing or invalid JWT token.
    *   `500 Internal Server Error`: Database or other server errors.

**3. Backend Structure:**

*   **Model:** Create `app/models/match.py` with a `Match` class to handle database interactions for the `Matches` table (similar to `app/models/user.py`). It should have at least a `save()` method.
*   **Service:** Create `app/services/match_service.py` with a `MatchService` class. This service will contain the business logic:
    *   `record_match(reporter_user_id, match_data)`:
        *   Validate `match_type`, player IDs (check existence, ensure players aren't duplicated across/within teams), scores.
        *   Determine `winner_team` (team with higher score).
        *   Determine `is_bagel` (if one score is 6 and the other is 0, or vice-versa).
        *   Create a `Match` object and call its `save()` method.
*   **Routes:** Create `app/routes/matches.py`.
    *   Define a new Flask Blueprint (`matches_bp`).
    *   Define the `POST /` route within the blueprint.
    *   Use the `@jwt_required()` decorator from `flask_jwt_extended`.
    *   Get the `reporter_user_id` from the JWT identity using `get_jwt_identity()`.
    *   Call the `MatchService.record_match` method.
*   **App Initialization:** Register the `matches_bp` in `app/__init__.py`.

This provides a solid foundation for the backend implementation. Next steps would involve writing the code for the Model, Service, and Routes.