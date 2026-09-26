from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("FootballSeasonTeamsProcessing") \
    .getOrCreate()

teams_raw_df = spark.read.option("multiLine", True).json(
    "data/raw/season_teams.json"
)

processed_teams = teams_raw_df.select(
    col("id").alias("team_id"),
    col("country_id"),
    col("venue_id"),
    col("founded"),
    col("gender"),
    col("type"),
    col("name").alias("team_name"),
    col("short_code"),
    col("last_played_at")
)

processed_teams.show(20, truncate=False)

processed_teams.write \
    .mode("overwrite") \
    .parquet("data/processed/season_teams")

print("Season teams processing: SUCCESS")
print("Teams processed:", processed_teams.count())

spark.stop()