from contextlib import closing
from typing import NamedTuple, List
import sqlalchemy
from sqlalchemy import create_engine
from sqlmodel import Session

from configuration.config import Config

class DatabaseColumn(NamedTuple):
    """
    This class represents a database column.
    """
    table: str
    column_name: str

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


    def get_all_columns(self) -> List[DatabaseColumn]:
        """Get all table name column name pairs in the database"""
        with Session(self.engine) as session:
            return []

    def get_all_text_columns(self) -> List[DatabaseColumn]:
        """Get all table name text column name pairs in the database"""
        with Session(self.engine) as session:
            return []

    def get_average_column_length(self, table: str, column: str) -> float:
        """Get average column length for a given table and column using DBCC SHOW_STATISTICS."""
        with closing(self.engine.raw_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DBCC SHOW_STATISTICS ({table}, {column}) WITH DENSITY_VECTOR")
            statistics_row = cursor.fetchall()
            return float(statistics_row[0][1]) # Average column length

