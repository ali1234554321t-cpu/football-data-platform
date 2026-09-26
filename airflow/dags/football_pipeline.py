from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="football_data_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["football", "data-engineering"],
) as dag:

    fetch_leagues = BashOperator(
        task_id="fetch_leagues",
        bash_command="cd /opt/football-data-platform && python ingestion/fetch_leagues.py",
    )

    fetch_teams = BashOperator(
        task_id="fetch_teams",
        bash_command="cd /opt/football-data-platform && python ingestion/fetch_season_teams.py",
    )

    fetch_fixtures = BashOperator(
        task_id="fetch_fixtures",
        bash_command="cd /opt/football-data-platform && python ingestion/fetch_fixtures.py",
    )

    fetch_events = BashOperator(
    task_id="fetch_fixture_events",
    bash_command="echo 'Using existing processed fixture events'",
   )

    fetch_players = BashOperator(
    task_id="fetch_fixture_players",
    bash_command="echo 'Using existing player data'",
    )

    transform_leagues = BashOperator(
        task_id="transform_leagues",
        bash_command="cd /opt/football-data-platform && python processing/transform_leagues.py",
    )

    transform_teams = BashOperator(
        task_id="transform_teams",
        bash_command="cd /opt/football-data-platform && python processing/transform_season_teams.py",
    )

    transform_fixtures = BashOperator(
        task_id="transform_fixtures",
        bash_command="cd /opt/football-data-platform && python processing/transform_fixtures.py",
    )

    transform_events = BashOperator(
        task_id="transform_events",
        bash_command="cd /opt/football-data-platform && python processing/transform_events.py",
    )

    transform_players = BashOperator(
        task_id="transform_players",
        bash_command="cd /opt/football-data-platform && python processing/transform_players.py",
    )

    transform_fixtures_enriched = BashOperator(
        task_id="transform_fixtures_enriched",
        bash_command="cd /opt/football-data-platform && python processing/transform_fixtures_enriched.py",
    )

    load_leagues = BashOperator(
        task_id="load_leagues",
        bash_command="cd /opt/football-data-platform && python ingestion/load_leagues_to_postgres.py",
    )

    load_teams = BashOperator(
        task_id="load_teams",
        bash_command="cd /opt/football-data-platform && python ingestion/load_teams_to_postgres.py",
    )

    load_players = BashOperator(
        task_id="load_players",
        bash_command="cd /opt/football-data-platform && python ingestion/load_players_to_postgres.py",
    )

    load_fixtures = BashOperator(
        task_id="load_fixtures",
        bash_command="cd /opt/football-data-platform && python ingestion/load_fixtures_to_postgres.py",
    )
    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="cd /opt/football-data-platform/dbt/football_dbt && dbt build",
    )

    load_events = BashOperator(
        task_id="load_fixture_events",
        bash_command="cd /opt/football-data-platform && python ingestion/load_fixture_events_to_postgres.py",
    )

    fetch_leagues >> transform_leagues >> load_leagues

    fetch_teams >> transform_teams >> load_teams

    fetch_fixtures >> transform_fixtures >> transform_fixtures_enriched >> load_fixtures

    fetch_events >> transform_events >> load_events

    fetch_players >> transform_players >> load_players
    [load_leagues, load_teams, load_players, load_fixtures, load_events] >> dbt_build
