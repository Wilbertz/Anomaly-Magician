from contextlib import closing
from dataclasses import dataclass
from typing import List

import sqlalchemy
from pydantic.v1 import PositiveInt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from codes.CodeModel import CodeModel
from configuration.config import Config

CONNECTION_STRING = (
    "mssql+pyodbc://@DESKTOP-2LMIUA2/Anomaly-Magician"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)

@dataclass(frozen=True)
class DatabaseColumn:
    """
    This class represents a database column. Schema is currently ignored.
    """
    table: str
    column_name: str

@dataclass(frozen=True)
class FixedLengthDatabaseColumn(DatabaseColumn):
    """This class represents a fixed length database column."""
    fixed_length: PositiveInt | None = None

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
        text_columns = [FixedLengthDatabaseColumn(
            table=column.table,
            column_name=column.column_name,
            fixed_length=self.is_fixed_length_column(column, tolerance))
            for column in self.get_all_text_columns()]
        return [column for column in text_columns if column.fixed_length]

    def get_all_distinct_column_values_in_buffer_pool(self, column: DatabaseColumn) -> List[str]:
        """Get all distinct column values that reside within the buffer pool."""
        sql = f"""
        SELECT
            DISTINCT t.{column.column_name} AS {column.column_name}
        FROM dbo.samplecodestable t
        CROSS APPLY sys.fn_PhysLocCracker(%%physloc%%) AS loc
        WHERE EXISTS (
            SELECT 1
            FROM sys.dm_os_buffer_descriptors bd
            JOIN sys.allocation_units au
                ON bd.allocation_unit_id = au.allocation_unit_id
            JOIN sys.partitions p
                ON au.container_id = p.hobt_id
            WHERE bd.database_id = DB_ID()
              AND p.object_id = OBJECT_ID('{column.table}')
              AND bd.file_id = loc.file_id
              AND bd.page_id = loc.page_id
        );
        """
        with sessionmaker(bind=self.engine)() as session:
            return [row[0] for row in session.execute(text(sql)).fetchall()]

    def get_all_distinct_column_values(self, column: DatabaseColumn, count: PositiveInt | None = None) -> List[str]:
        """Get all distinct column values."""
        sql = f"""
        SELECT DISTINCT {column.column_name} AS {column.column_name}
        FROM {column.table}
        """
        result = []
        with sessionmaker(bind=self.engine)() as session:
            result = [row[0] for row in session.execute(text(sql)).fetchall()]

        return result

    def clean_buffer_pool(self) -> None:
        """To test the buffer pool related commands, the buffer pool is cleaned."""
        with sessionmaker(bind=self.engine)() as session:
            session.execute(text('DBCC DROPCLEANBUFFERS'))

    def read_complete_table(self, table: str) -> None:
        """Read the complete table. All or a significant number of rows should now reside within the buffer pool."""
        with sessionmaker(bind=self.engine)() as session:
            session.execute(text(f'SELECT * FROM {table}'))

    def check_column_values_against_code(self, column: DatabaseColumn, code: CodeModel) -> bool:
        """
        Check a given database column against the given code
        :param column: The database column to check
        :param code: The code against the check is done.
        :return:
        """
        # First: use statistics information
        average_column_length = self.get_average_column_length(column)
        if average_column_length < code.min_length or average_column_length > code.max_length:
            return False

        # Second: use the columns within the buffer pool
        column_values = self.get_all_distinct_column_values_in_buffer_pool(column)
        if any(lambda x: not code.simple_check(x) for x in column_values):
            return False

        # Third: use the full database table.
        column_values = self.get_all_distinct_column_values(column)
        if any(lambda x: not code.simple_check(x) for x in column_values):
            return False

        return True