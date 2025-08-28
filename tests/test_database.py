import os
from pathlib import Path
import pytest

from configuration.config import Config
from database.database import Database, DatabaseColumn, FixedLengthDatabaseColumn


@pytest.fixture(autouse=True)
def run_before_tests(monkeypatch):
    monkeypatch.chdir(Path(os.getcwd()).parent)

def test_dummy():
    assert 1 == 1

def test_database_singleton():
    database1 = Database()
    assert database1
    database2 = Database()
    assert database1 == database2

def test_get_connection_string():
    database = Database()
    connections_string = database._get_connection_string()
    assert connections_string

def test_get_engine():
    database = Database()
    engine = database._get_engine()
    assert engine

def test_get_all_columns():
    database = Database()
    all_columns = database.get_all_columns()
    print (all_columns)
    assert len(all_columns) == 2

def test_get_all_text_columns():
    database = Database()
    all_columns = database.get_all_text_columns()
    print (all_columns)
    assert len(all_columns) == 1

def test_is_fixed_length_column():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    is_fixed_length = database.is_fixed_length_column(database_column)
    assert is_fixed_length is None

def test_is_fixed_length_column_with_tolerance():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    is_fixed_length = database.is_fixed_length_column(database_column, tolerance=0.1)
    assert is_fixed_length == 5

def test_get_all_fixed_length_columns():
    database = Database()
    columns = database.get_all_fixed_length_columns()
    assert len(columns) == 0

def test_get_all_fixed_length_columns_with_tolerance():
    database = Database()
    columns = database.get_all_fixed_length_columns(tolerance=1.0)
    print (columns[0])
    assert len(columns) == 1

def test_get_average_column_length():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    average_column_length = database.get_average_column_length(database_column)
    assert average_column_length > 0

