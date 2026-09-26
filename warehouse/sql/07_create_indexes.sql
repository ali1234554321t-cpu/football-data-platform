CREATE INDEX IF NOT EXISTS idx_fact_fixtures_date_key
ON fact_fixtures(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixtures_league_key
ON fact_fixtures(league_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixtures_home_team_key
ON fact_fixtures(home_team_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixtures_away_team_key
ON fact_fixtures(away_team_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixture_events_fixture_key
ON fact_fixture_events(fixture_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixture_events_player_key
ON fact_fixture_events(player_key);

CREATE INDEX IF NOT EXISTS idx_fact_fixture_events_related_player_key
ON fact_fixture_events(related_player_key);