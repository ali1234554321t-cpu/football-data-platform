CREATE TABLE IF NOT EXISTS dim_team (
    team_key SERIAL PRIMARY KEY,
    team_id BIGINT NOT NULL,
    team_name VARCHAR(255) NOT NULL,
    short_code VARCHAR(20),
    country_id BIGINT,
    venue_id BIGINT,
    founded INTEGER,
    gender VARCHAR(20),
    team_type VARCHAR(50),
    last_played_at TIMESTAMP
);