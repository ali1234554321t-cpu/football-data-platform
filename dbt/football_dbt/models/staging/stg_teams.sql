select
    team_key,
    team_id,
    team_name,
    short_code,
    country_id,
    venue_id,
    founded,
    gender,
    team_type,
    last_played_at
from {{ source('football_warehouse', 'dim_team') }}