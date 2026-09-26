from pyspark.sql import SparkSession
import psycopg2


spark = SparkSession.builder \
    .appName("LoadPlayersToPostgres") \
    .getOrCreate()


df = spark.read.parquet("data/processed/players")
rows = df.collect()

print("Players read from Parquet:", len(rows))


connection = psycopg2.connect(
    host="host.docker.internal",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

cursor = connection.cursor()


cursor.execute("DROP TABLE IF EXISTS players")

cursor.execute("""
    CREATE TABLE players (
        player_id BIGINT PRIMARY KEY,
        country_id BIGINT,
        nationality_id BIGINT,
        position_id BIGINT,
        detailed_position_id BIGINT,
        height INTEGER,
        weight INTEGER,
        date_of_birth DATE,
        gender VARCHAR(20),
        common_name VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        name VARCHAR(255),
        display_name VARCHAR(255),
        image_path TEXT
    )
""")


for row in rows:
    cursor.execute("""
        INSERT INTO players (
            player_id,
            country_id,
            nationality_id,
            position_id,
            detailed_position_id,
            height,
            weight,
            date_of_birth,
            gender,
            common_name,
            firstname,
            lastname,
            name,
            display_name,
            image_path
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s
        )
    """, (
        row["player_id"],
        row["country_id"],
        row["nationality_id"],
        row["position_id"],
        row["detailed_position_id"],
        row["height"],
        row["weight"],
        row["date_of_birth"],
        row["gender"],
        row["common_name"],
        row["firstname"],
        row["lastname"],
        row["name"],
        row["display_name"],
        row["image_path"]
    ))


connection.commit()

print("Players loaded into PostgreSQL successfully")
print("Rows loaded:", len(rows))


cursor.close()
connection.close()
spark.stop()
