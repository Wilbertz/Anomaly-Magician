from contextlib import closing

import sqlalchemy
from sqlalchemy import create_engine
from configuration.config import Config


class Database:
    """
    This class (implemented as a singleton) implements access to the database analyzed.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.engine = self._get_engine()
        pass

    @staticmethod
    def _get_connection_string() -> str:
        connection_string = (
            f"mssql+pyodbc://@{Config().server}/{Config().database}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&trusted_connection=yes"
        )
        return connection_string

    def _get_engine(self) -> sqlalchemy.engine.Engine:
        connection_string = self._get_connection_string()
        engine = create_engine(connection_string, echo=False)
        return engine

    def get_statistics(self):
        with closing(self.engine.raw_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DBCC SHOW_STATISTICS ('samplecodestable', 'value')")
            rows1 = cursor.fetchall()
            print(rows1)
            cursor.nextset()
            rows2 = cursor.fetchall()
            print(rows2)
            print(f"Average length: {rows2[0][1]}")
            cursor.nextset()
            rows3 = cursor.fetchall()
            print(rows3)
