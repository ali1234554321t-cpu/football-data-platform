select
    event_key,
    event_id,
    fixture_key,
    player_key,
    related_player_key,
    event_type_id,
    minute,
    extra_minute,
    result,
    info,
    addition
from {{ source('football_warehouse', 'fact_fixture_events') }}