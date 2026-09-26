select
    league_key,
    league_id,
    league_name,
    country_id,
    country_name,
    league_type
from {{ source('football_warehouse', 'dim_league') }}