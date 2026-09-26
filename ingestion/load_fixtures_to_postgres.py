from pyspark.sql import SparkSession
import psycopg2


spark = SparkSession.builder \
    .appName("LoadFixturesToPostgres") \
    .getOrCreate()


# Read processed fixtures using Spark
df = spark.read.parquet("data/processed/fixtures_enriched")

rows = df.collect()

print("Fixtures read from Parquet:", len(rows))


# Connect to PostgreSQL
connection = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

cursor = connection.cursor()


# Recreate fixtures table
cursor.execute("DROP TABLE IF EXISTS fixtures")

cursor.execute("""
    CREATE TABLE fixtures (
        fixture_id BIGINT PRIMARY KEY,
        league_id BIGINT,
        season_id BIGINT,
        stage_id BIGINT,
        round_id BIGINT,
        venue_id BIGINT,
        name VARCHAR(255),
        starting_at TIMESTAMP,
        result_info VARCHAR(255),
        leg VARCHAR(20),
        length INTEGER,
        home_team_id BIGINT,
        home_team_name VARCHAR(255),
        home_winner BOOLEAN,
        away_team_id BIGINT,
        away_team_name VARCHAR(255),
        away_winner BOOLEAN
    )
""")


# Insert fixtures
for row in rows:

    cursor.execute("""
        INSERT INTO fixtures (
            fixture_id,
            league_id,
            season_id,
            stage_id,
            round_id,
            venue_id,
            name,
            starting_at,
            result_info,
            leg,
            length,
            home_team_id,
            home_team_name,
            home_winner,
            away_team_id,
            away_team_name,
            away_winner
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        row["fixture_id"],
        row["league_id"],
        row["season_id"],
        row["stage_id"],
        row["round_id"],
        row["venue_id"],
        row["name"],
        row["starting_at"],
        row["result_info"],
        row["leg"],
        row["length"],
        row["home_team_id"],
        row["home_team_name"],
        row["home_winner"],
        row["away_team_id"],
        row["away_team_name"],
        row["away_winner"]
    ))


connection.commit()

print("Fixtures loaded into PostgreSQL successfully")
print("Rows loaded:", len(rows))


cursor.close()
connection.close()
spark.stop()
