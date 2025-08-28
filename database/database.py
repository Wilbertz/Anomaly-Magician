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


    def get_average_column_length(self, table: str, column: str) -> float:
        with closing(self.engine.raw_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute("DBCC SHOW_STATISTICS ('samplecodestable', 'value') WITH DENSITY_VECTOR")
            statistics_row = cursor.fetchall()
            return float(statistics_row[0][1]) # Average column length

