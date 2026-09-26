from pyspark.sql import SparkSession
import psycopg2

spark = SparkSession.builder     .appName("LoadFixtureEventsToPostgres")     .getOrCreate()

df = spark.read.parquet("data/processed/fixture_events")
rows = df.collect()

print("Fixture events read from Parquet:", len(rows))

connection = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS fixture_events")

cursor.execute("""
    CREATE TABLE fixture_events (
        event_id BIGINT PRIMARY KEY,
        fixture_id BIGINT,
        player_id BIGINT,
        player_name VARCHAR(255),
        related_player_id BIGINT,
        related_player_name VARCHAR(255),
        type_id BIGINT,
        minute INTEGER,
        extra_minute INTEGER,
        result VARCHAR(255),
        info VARCHAR(255),
        addition VARCHAR(255)
    )
""")

for row in rows:
    cursor.execute("""
        INSERT INTO fixture_events (
            event_id,
            fixture_id,
            player_id,
            player_name,
            related_player_id,
            related_player_name,
            type_id,
            minute,
            extra_minute,
            result,
            info,
            addition
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """, (
        row["event_id"],
        row["fixture_id"],
        row["player_id"],
        row["player_name"],
        row["related_player_id"],
        row["related_player_name"],
        row["type_id"],
        row["minute"],
        row["extra_minute"],
        row["result"],
        row["info"],
        row["addition"]
    ))

connection.commit()

print("Fixture events loaded into PostgreSQL successfully")
print("Rows loaded:", len(rows))

cursor.close()
connection.close()
spark.stop()
