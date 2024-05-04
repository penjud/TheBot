import psycopg2
conn = None
try:
    conn = psycopg2.connect(
        host="localhost",
        database="thebot",
        user="penjud",
        password="#18Hoppy70"
    )
    cur = conn.cursor()
    cur.execute('SELECT 1')
    if cur.fetchone():
        print("Database connection successful.")
    cur.close()
except Exception as e:
    print(f"Database connection failed: {e}")
finally:
    if conn is not None:
        conn.close()
