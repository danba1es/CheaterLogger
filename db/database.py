import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.connection_params = {
            'dbname': os.getenv('PGDATABASE'),
            'user': os.getenv('PGUSER'),
            'password': os.getenv('PGPASSWORD'),
            'host': os.getenv('PGHOST'),
            'port': os.getenv('PGPORT')
        }

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(**self.connection_params)
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query, params=None):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                conn.commit()
                try:
                    return cur.fetchall()
                except psycopg2.ProgrammingError:
                    return None

    def initialize_tables(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS cheaters (
                id SERIAL PRIMARY KEY,
                gamertag VARCHAR(100) NOT NULL,
                reporter_id BIGINT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_banned BOOLEAN DEFAULT FALSE,
                map_location VARCHAR(200),
                base_location VARCHAR(200),
                spi_command VARCHAR(200)
            )
            """
        ]
        
        for query in queries:
            self.execute_query(query)
