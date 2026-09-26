from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("FootballPlayersProcessing") \
    .getOrCreate()

players_raw_df = spark.read.option("multiLine", True).json(
    "data/raw/fixture_players.json"
)

processed_players = players_raw_df.select(
    col("id").alias("player_id"),
    col("country_id"),
    col("nationality_id"),
    col("position_id"),
    col("detailed_position_id"),
    col("height"),
    col("weight"),
    col("date_of_birth"),
    col("gender"),
    col("common_name"),
    col("firstname"),
    col("lastname"),
    col("name"),
    col("display_name"),
    col("image_path")
)

processed_players.show(10, truncate=False)

processed_players.write \
    .mode("overwrite") \
    .parquet("data/processed/players")

print("Players processing: SUCCESS")
print("Players processed:", processed_players.count())

spark.stop()