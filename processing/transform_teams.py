from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("FootballTeamsProcessing") \
    .getOrCreate()

# Read raw teams
teams_raw_df = spark.read.option("multiLine", True).json(
    "data/raw/teams.json"
)

teams_df = teams_raw_df.selectExpr("explode(data) as team").select("team.*")

# Select important columns
processed_teams = teams_df.select(
    col("id").alias("team_id"),
    col("country_id"),
    col("venue_id"),
    col("founded"),
    col("gender"),
    col("type"),
    col("last_played_at")
)

# Show processed data
processed_teams.show(10, truncate=False)

# Write processed data as Parquet
processed_teams.write \
    .mode("overwrite") \
    .parquet("data/processed/teams")

spark.stop()