with fixtures as (

    select *
    from {{ ref('stg_fixtures') }}

),

leagues as (

    select *
    from {{ ref('stg_leagues') }}

),

teams as (

    select *
    from {{ ref('stg_teams') }}

),

dates as (

    select *
    from {{ ref('stg_dates') }}

)

select
    f.fixture_key,
    f.fixture_id,

    d.full_date,
    d.year_number,
    d.month_name,
    d.quarter_number,

    l.league_id,
    l.league_name,

    home.team_id as home_team_id,
    home.team_name as home_team_name,

    away.team_id as away_team_id,
    away.team_name as away_team_name,

    f.fixture_name,
    f.starting_at,
    f.venue_id,
    f.status,

    f.home_score,
    f.away_score,
    f.home_winner,
    f.away_winner

from fixtures f

left join leagues l
    on f.league_key = l.league_key

left join teams home
    on f.home_team_key = home.team_key

left join teams away
    on f.away_team_key = away.team_key

left join dates d
    on f.date_key = d.date_key