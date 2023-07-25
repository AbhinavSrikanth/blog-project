import psycopg2
from psycopg2 import OperationalError

class Database:
    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance=super(Database,cls).__new__(cls)
            cls._instance.connection=cls._instance.connect()
        return cls._instance

    def connect(cls):
        try:
            connection=psycopg2.connect(
                dbname='blog',
                user='whirldata',
                password='Whirldata@123',
                host='localhost',
                port='5432'
            )
            connection.autocommit=True
            print("Connected to the Database")
            return connection
        except OperationalError as e:
            print(f"Error:{e}")
            return None
        
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection Closed")