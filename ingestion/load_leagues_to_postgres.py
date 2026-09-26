from pyspark.sql import SparkSession
import psycopg2

spark = SparkSession.builder     .appName("LoadLeaguesToPostgres")     .getOrCreate()

df = spark.read.parquet("data/processed/leagues")
rows = df.collect()

print("Leagues read from Parquet:", len(rows))

connection = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS leagues")

cursor.execute("""
    CREATE TABLE leagues (
        league_id BIGINT PRIMARY KEY,
        sport_id BIGINT,
        country_id BIGINT,
        name VARCHAR(255),
        active BOOLEAN,
        short_code VARCHAR(20)
    )
""")

for row in rows:
    cursor.execute("""
        INSERT INTO leagues (
            league_id,
            sport_id,
            country_id,
            name,
            active,
            short_code
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        row["league_id"],
        row["sport_id"],
        row["country_id"],
        row["name"],
        row["active"],
        row["short_code"]
    ))

connection.commit()

print("Leagues loaded into PostgreSQL successfully")
print("Rows loaded:", len(rows))

cursor.close()
connection.close()
spark.stop()
