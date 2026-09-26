import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="football_db",
    user="football_user",
    password="football_password"
)

print("PostgreSQL connection: SUCCESS")

connection.close()