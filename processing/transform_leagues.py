from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("FootballLeaguesProcessing") \
    .getOrCreate()

# Read raw leagues
leagues_raw_df = spark.read.option("multiLine", True).json(
    "data/raw/leagues.json"
)

# Extract leagues from API response
leagues_df = leagues_raw_df.selectExpr(
    "explode(data) as league"
).select("league.*")

# Select important columns
processed_leagues = leagues_df.select(
    col("id").alias("league_id"),
    col("sport_id"),
    col("country_id"),
    col("name"),
    col("active"),
    col("short_code")
)

# Show processed data
processed_leagues.show(10, truncate=False)

# Write processed data as Parquet
processed_leagues.write \
    .mode("overwrite") \
    .parquet("data/processed/leagues")

spark.stop()