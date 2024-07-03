CREATE TABLE players(
    user_id int NOT NULL, 
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL, 
    wins int NOT NULL, 
    losses int NOT NULL, 
    draws int NOT NULL, 
    email VARCHAR(255), 
    phone number VARCHAR(15), 
    current_match_id int
);
CREATE TABLE tournaments(
    winner_id int REFERENCES players(user_id) UNIQUE user_id, 
    tournament_id int NOT NULL
    tournament_status VARCHAR(20) NOT NULL
);
CREATE TABLE matches(
    match_id, 
    tournament_id player1_id NOT NULL,
    round int NOT NULL,
    player2_id, player1_wins int NOT NULL,
    player1_losses int NOT NULL,
    player1_draws int NOT NULL
);