CREATE TABLE players(
    user_id SERIAL UNIQUE, 
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL, 
    wins int NOT NULL, 
    losses int NOT NULL, 
    draws int NOT NULL, 
    email VARCHAR(255), 
    phone_number VARCHAR(15), 
    current_match_id int
);



CREATE TABLE tournaments(
    winner_id int REFERENCES players(user_id), 
    tournament_id SERIAL UNIQUE,
    tournament_status VARCHAR(20) NOT NULL
);

CREATE TABLE matches(
    round int NOT NULL,
    match_id SERIAL,
    id int REFERENCES tournaments (tournament_id),
    player1_id int REFERENCES players(user_id) UNIQUE NOT NULL,
    player2_id int, 
    player1_wins int NOT NULL,
    player1_losses int NOT NULL,
    player1_draws int NOT NULL
);



