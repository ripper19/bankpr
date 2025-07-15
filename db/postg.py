import psycopg2
from psycopg2 import OperationalError

class PostConnection:
    _instance = None
    def __new__(cls, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        try:
            cls._instance.conn = psycopg2.connect(
                host = DB_HOST, 
                port = DB_PORT,
                dbname = DB_NAME,
                user = DB_USER,
                password = DB_PASSWORD
            )
            cls._instance.conn.autocommit = False
        except OperationalError as e:
            raise ConnectionError(str(e))
        return cls._instance
    def get_cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()