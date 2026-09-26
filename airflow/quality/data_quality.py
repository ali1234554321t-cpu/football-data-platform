import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="football_dw",
    user="football_user",
    password="football_password"
)

cur = conn.cursor()

print("\n=== DATA QUALITY CHECKS ===\n")

# Row counts
tables = [
    "dim_date",
    "dim_league",
    "dim_team",
    "dim_player",
    "fact_fixtures",
    "fact_fixture_events"
]

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    print(f"{table}: {count} rows")


# Duplicate fixture IDs
cur.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT fixture_id
        FROM fact_fixtures
        GROUP BY fixture_id
        HAVING COUNT(*) > 1
    ) duplicates
""")

duplicates = cur.fetchone()[0]

print(f"\nDuplicate fixtures: {duplicates}")


# NULL fixture IDs
cur.execute("""
    SELECT COUNT(*)
    FROM fact_fixtures
    WHERE fixture_id IS NULL
""")

null_fixtures = cur.fetchone()[0]

print(f"NULL fixture IDs: {null_fixtures}")


# Orphan fixture events
cur.execute("""
    SELECT COUNT(*)
    FROM fact_fixture_events e
    LEFT JOIN fact_fixtures f
        ON e.fixture_key = f.fixture_key
    WHERE f.fixture_key IS NULL
""")

orphan_events = cur.fetchone()[0]

print(f"Orphan events: {orphan_events}")


# Final status
if duplicates == 0 and null_fixtures == 0 and orphan_events == 0:
    print("\nDATA QUALITY: PASSED")
else:
    print("\nDATA QUALITY: FAILED")

cur.close()
conn.close()