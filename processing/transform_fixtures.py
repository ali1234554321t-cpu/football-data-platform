from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("FootballFixturesProcessing") \
    .getOrCreate()

# Read raw fixtures
fixtures_df = spark.read.option("multiLine", True).json(
    "data/raw/fixtures.json"
)

# Select important columns
processed_fixtures = fixtures_df.select(
    col("id").alias("fixture_id"),
    col("league_id"),
    col("season_id"),
    col("stage_id"),
    col("round_id"),
    col("venue_id"),
    col("name"),
    col("starting_at"),
    col("result_info"),
    col("leg"),
    col("length"),
    col("placeholder"),
    col("starting_at_timestamp")
)

# Show processed data
processed_fixtures.show(10, truncate=False)

# Write processed data as Parquet
processed_fixtures.write \
    .mode("overwrite") \
    .parquet("data/processed/fixtures")

spark.stop()