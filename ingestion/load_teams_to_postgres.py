from pyspark.sql import SparkSession
import psycopg2


spark = SparkSession.builder \
    .appName("LoadTeamsToPostgres") \
    .getOrCreate()


df = spark.read.parquet("data/processed/season_teams")
rows = df.collect()

print("Teams read from Parquet:", len(rows))


connection = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

cursor = connection.cursor()


cursor.execute("DROP TABLE IF EXISTS teams")

cursor.execute("""
    CREATE TABLE teams (
        team_id BIGINT PRIMARY KEY,
        country_id BIGINT,
        venue_id BIGINT,
        founded INTEGER,
        gender VARCHAR(20),
        type VARCHAR(50),
        team_name VARCHAR(255),
        short_code VARCHAR(20),
        last_played_at TIMESTAMP
    )
""")


for row in rows:
    cursor.execute("""
        INSERT INTO teams (
            team_id,
            country_id,
            venue_id,
            founded,
            gender,
            type,
            team_name,
            short_code,
            last_played_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["team_id"],
        row["country_id"],
        row["venue_id"],
        row["founded"],
        row["gender"],
        row["type"],
        row["team_name"],
        row["short_code"],
        row["last_played_at"]
    ))


connection.commit()

print("Teams loaded into PostgreSQL successfully")
print("Rows loaded:", len(rows))


cursor.close()
connection.close()
spark.stop()
