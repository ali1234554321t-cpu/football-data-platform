with events as (

    select *
    from {{ ref('stg_fixture_events') }}

),

players as (

    select *
    from {{ ref('stg_players') }}

),

fixtures as (

    select *
    from {{ ref('fct_matches') }}

)

select
    e.event_key,
    e.event_id,

    f.fixture_id,
    f.full_date,
    f.league_name,
    f.home_team_name,
    f.away_team_name,

    p.player_id,
    p.player_name,

    rp.player_id as related_player_id,
    rp.player_name as related_player_name,

    e.event_type_id,
    e.minute,
    e.extra_minute,
    e.result,
    e.info,
    e.addition

from events e

left join players p
    on e.player_key = p.player_key

left join players rp
    on e.related_player_key = rp.player_key

left join fixtures f
    on e.fixture_key = f.fixture_key