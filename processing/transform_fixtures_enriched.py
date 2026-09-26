from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, when

spark = SparkSession.builder \
    .appName("FootballFixturesEnrichedProcessing") \
    .getOrCreate()

# Read enriched fixtures
fixtures_df = spark.read.option("multiLine", True).json(
    "data/raw/fixtures_enriched.json"
)

# Explode participants
participants_df = fixtures_df.select(
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
    explode("participants").alias("participant")
)

# Extract home and away teams
home_df = participants_df.filter(
    col("participant.meta.location") == "home"
).select(
    "fixture_id",
    col("participant.id").alias("home_team_id"),
    col("participant.name").alias("home_team_name"),
    col("participant.meta.winner").alias("home_winner")
)

away_df = participants_df.filter(
    col("participant.meta.location") == "away"
).select(
    "fixture_id",
    col("participant.id").alias("away_team_id"),
    col("participant.name").alias("away_team_name"),
    col("participant.meta.winner").alias("away_winner")
)

# Join home and away teams
processed_fixtures = participants_df.select(
    "fixture_id",
    "league_id",
    "season_id",
    "stage_id",
    "round_id",
    "venue_id",
    "name",
    "starting_at",
    "result_info",
    "leg",
    "length"
).dropDuplicates(["fixture_id"]) \
.join(home_df, on="fixture_id", how="left") \
.join(away_df, on="fixture_id", how="left")

processed_fixtures.show(10, truncate=False)

# Save as Parquet
processed_fixtures.write \
    .mode("overwrite") \
    .parquet("data/processed/fixtures_enriched")

print("Fixtures enrichment processing: SUCCESS")
print("Fixtures processed:", processed_fixtures.count())

spark.stop()