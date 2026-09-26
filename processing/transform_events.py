from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FootballEventsProcessing") \
    .getOrCreate()

events_df = spark.read.parquet(
    "data/processed/fixture_events"
)

print("Events processing: SUCCESS")
print("Events available:", events_df.count())

events_df.show(10, truncate=False)

spark.stop()