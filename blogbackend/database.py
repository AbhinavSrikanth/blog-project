import psycopg2
from psycopg2 import OperationalError

class Database:
    def __init__(self):
        self.connection = self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def connect(self):
        try:
            connection = psycopg2.connect(
                dbname='blog',
                user='whirldata',
                password='Whirldata@123',
                host='localhost',
                port='5432'
            )
            connection.autocommit = True
            print("Connected to the Database")
            return connection
        except OperationalError as e:
            print(f"Error: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection Closed")
