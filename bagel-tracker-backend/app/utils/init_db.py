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
    
    # Execute query
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
    
    # Execute query
    execute_query(matches_table_query, fetch=False)
    
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()