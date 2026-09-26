select
    player_key,
    player_id,
    player_name
from {{ source('football_warehouse', 'dim_player') }}