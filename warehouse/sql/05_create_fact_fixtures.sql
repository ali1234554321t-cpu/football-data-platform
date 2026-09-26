CREATE TABLE IF NOT EXISTS fact_fixtures (
    fixture_key SERIAL PRIMARY KEY,
    fixture_id BIGINT NOT NULL,
    date_key INTEGER,
    league_key INTEGER,
    home_team_key INTEGER,
    away_team_key INTEGER,

    fixture_name VARCHAR(255),
    starting_at TIMESTAMP,
    venue_id BIGINT,
    status VARCHAR(100),

    home_score INTEGER,
    away_score INTEGER,
    home_winner BOOLEAN,
    away_winner BOOLEAN,

    CONSTRAINT fk_fixture_date
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key),

    CONSTRAINT fk_fixture_league
        FOREIGN KEY (league_key) REFERENCES dim_league(league_key),

    CONSTRAINT fk_fixture_home_team
        FOREIGN KEY (home_team_key) REFERENCES dim_team(team_key),

    CONSTRAINT fk_fixture_away_team
        FOREIGN KEY (away_team_key) REFERENCES dim_team(team_key)
);