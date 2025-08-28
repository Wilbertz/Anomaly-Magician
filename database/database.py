from contextlib import closing
from typing import NamedTuple, List

import sqlalchemy
from pydantic.v1 import PositiveInt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from configuration.config import Config


class DatabaseColumn(NamedTuple):
    """
    This class represents a database column. Schema is currently ignored.
    """
    table: str
    column_name: str

class FixedLengthDatabaseColumn(DatabaseColumn):
    """This class represents a fixed length database column."""
    fixed_length: PositiveInt

    def __new__(cls, table, column_name, fixed_length):
        return (super(FixedLengthDatabaseColumn, cls).
                __new__(cls, table, column_name), fixed_length)

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
        sql = """
        SELECT 
            s.name AS SchemaName, 
            t.name AS TableName, 
            c.name AS ColumnName,
            ty.name AS DataType
        FROM sys.columns c
        JOIN sys.tables t ON c.object_id = t.object_id
        JOIN sys.schemas s ON t.schema_id = s.schema_id
        JOIN sys.types ty ON c.user_type_id = ty.user_type_id
        """
        with sessionmaker(bind=self.engine)() as session:
            return [DatabaseColumn(row[1], row[2]) for row in session.execute(text(sql)).fetchall()]

    def get_all_text_columns(self) -> List[DatabaseColumn]:
        """Get all table name text column name pairs in the database"""
        sql = """
              SELECT s.name  AS SchemaName, 
                     t.name  AS TableName, 
                     c.name  AS ColumnName, 
                     ty.name AS DataType
              FROM sys.columns c
                       JOIN sys.tables t ON c.object_id = t.object_id
                       JOIN sys.schemas s ON t.schema_id = s.schema_id
                       JOIN sys.types ty ON c.user_type_id = ty.user_type_id 
              WHERE UPPER(ty.name) LIKE '%CHAR%' OR ty.name LIKE '%TEXT%'
              """
        with sessionmaker(bind=self.engine)() as session:
            return [DatabaseColumn(row[1], row[2]) for row in session.execute(text(sql)).fetchall()]

    def get_average_column_length(self, column: DatabaseColumn) -> float:
        """Get average column length for a given table and column using DBCC SHOW_STATISTICS."""
        with closing(self.engine.raw_connection()) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DBCC SHOW_STATISTICS ({column.table}, {column.column_name}) WITH DENSITY_VECTOR")
            statistics_row = cursor.fetchall()
            return float(statistics_row[0][1]) # Average column length

    def is_fixed_length_column(self, column: DatabaseColumn, tolerance: float = 0) -> int | None:
        """Check if a column has a fixed length. In case the column has a fixed length, its length is returned."""
        length = self.get_average_column_length(column)
        nearest = round(length)
        if abs(length - nearest) <= tolerance:
            return nearest
        return None

    def get_all_fixed_length_columns(self, tolerance: float = 0) -> List[FixedLengthDatabaseColumn]:
        """ Get all text columns with a fixed length."""
        text_columns = self.get_all_text_columns()
        return [FixedLengthDatabaseColumn(
            table=column.table,
            column_name=column.column_name,
            fixed_length=self.is_fixed_length_column(column, tolerance))
            for column in text_columns]