CREATE TABLE players(
    user_id SERIAL UNIQUE, 
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL, 
    wins int DEFAULT 0 NOT NULL, 
    losses int DEFAULT 0 NOT NULL, 
    draws int DEFAULT 0 NOT NULL, 
    email VARCHAR(255), 
    phone_number VARCHAR(15), 
    looking_for_match BOOLEAN
);
ALTER table players ALTER COLUMN looking_for_match SET DEFAULT false;



CREATE TABLE tournaments(
    winner_id int REFERENCES players(user_id), 
    tournament_id SERIAL UNIQUE,
    tournament_round int NOT NULL
);

CREATE TABLE matches(
    round int NOT NULL,
    match_id SERIAL,
    id int REFERENCES tournaments (tournament_id),
    player1_id int REFERENCES players(user_id) NOT NULL,
    player2_id int, 
    player1_wins int DEFAULT 0 NOT NULL,
    player1_losses int DEFAULT 0 NOT NULL,
    player1_draws int DEFAULT 0 NOT NULL,
    complete BOOLEAN NOT NULL
);



