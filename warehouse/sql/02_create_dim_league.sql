CREATE TABLE IF NOT EXISTS dim_league (
    league_key SERIAL PRIMARY KEY,
    league_id BIGINT NOT NULL,
    league_name VARCHAR(255) NOT NULL,
    country_id BIGINT,
    country_name VARCHAR(255),
    league_type VARCHAR(100)
);