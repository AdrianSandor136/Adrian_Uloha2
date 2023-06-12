import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def initialize_database():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exchange_history (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                from_currency VARCHAR(3) NOT NULL,
                to_currency VARCHAR(3) NOT NULL,
                exchange_rate DECIMAL(10, 2) NOT NULL,
                is_higher BOOLEAN NOT NULL
            )
        ''')
    conn.commit()

    return conn
