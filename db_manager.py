import sqlite3
from sqlite3 import Connection
from threading import Lock

class DatabaseConnection:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_instance(cls) -> Connection:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = sqlite3.connect('driving_simulations.db', check_same_thread=False)
                    cls._instance.row_factory = sqlite3.Row
        return cls._instance

    @classmethod
    def close_connection(cls):
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None

# Global function to get the database connection
def get_db() -> Connection:
    return DatabaseConnection.get_instance()