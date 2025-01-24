import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="library_management",
            user="postgres",
            password="soham0500",
            host="localhost",
            port="5432"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Database connection failed: {e}")
        return None
