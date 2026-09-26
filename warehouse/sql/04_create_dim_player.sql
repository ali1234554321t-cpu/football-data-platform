CREATE TABLE IF NOT EXISTS dim_player (
    player_key SERIAL PRIMARY KEY,
    player_id BIGINT NOT NULL,
    player_name VARCHAR(255) NOT NULL
);