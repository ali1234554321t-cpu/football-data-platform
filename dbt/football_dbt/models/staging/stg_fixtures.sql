select
    fixture_key,
    fixture_id,
    date_key,
    league_key,
    home_team_key,
    away_team_key,
    fixture_name,
    starting_at,
    venue_id,
    status,
    home_score,
    away_score,
    home_winner,
    away_winner
from {{ source('football_warehouse', 'fact_fixtures') }}