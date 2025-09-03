import os
from pathlib import Path

import pytest

from codes.VinCode import VinCode
from configuration.config import Config
from database.database import Database, DatabaseColumn


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
    assert len(all_columns) == 6

def test_get_all_text_columns():
    database = Database()
    all_columns = database.get_all_text_columns()
    assert len(all_columns) == 4

def test_column_has_statistics():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    has_statistics = database.column_has_statistics(database_column)
    assert has_statistics

def test_is_fixed_length_column():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    is_fixed_length = database.is_fixed_length_column(database_column)
    assert is_fixed_length

def test_is_not_fixed_length_column():
    database = Database()
    database_column = DatabaseColumn(Config().table, "vin_invalid_length")
    is_fixed_length = database.is_fixed_length_column(database_column)
    assert is_fixed_length

def test_is_fixed_length_column_with_tolerance():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    is_fixed_length = database.is_fixed_length_column(database_column, tolerance=0.1)
    assert is_fixed_length == 17

def test_get_all_fixed_length_columns():
    database = Database()
    columns = database.get_all_fixed_length_columns()
    assert len(columns) == 3

def test_get_all_fixed_length_columns_with_tolerance():
    database = Database()
    columns = database.get_all_fixed_length_columns(tolerance=1.0)
    assert len(columns) == 4

def test_get_average_column_length():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    average_column_length = database.get_average_column_length(database_column)
    assert average_column_length > 0

def test_get_average_column_length_without_statistics():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    average_column_length = database.get_average_column_length(database_column)
    assert average_column_length == 17.0

def test_get_all_distinct_column_values_in_clean_buffer_pool():
    database = Database()
    database.clean_buffer_pool()
    database_column = DatabaseColumn(Config().table, Config().column)
    _ = database.get_all_distinct_column_values_in_buffer_pool(database_column)

def test_get_all_distinct_column_values_in_filled_buffer_pool():
    database = Database()
    database.read_complete_table(Config().table)
    database_column = DatabaseColumn(Config().table, Config().column)
    values =database.get_all_distinct_column_values_in_buffer_pool(database_column)
    assert len(values) == 10000

def test_get_all_distinct_column_values():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    values = database.get_all_distinct_column_values(database_column)
    assert len(values) == 10000

def test_check_valid_column_values_against_code():
    database = Database()
    database_column = DatabaseColumn(Config().table, Config().column)
    code = VinCode()
    result = database.check_column_values_against_code(database_column, code)
    assert result == True

def test_check_invalid_regex_column_values_against_code():
    database = Database()
    database_column = DatabaseColumn(Config().table, "vin_valid_length_invalid_regex")
    code = VinCode()
    result = database.check_column_values_against_code(database_column, code)
    assert result == False

def test_check_invalid_length_column_values_against_code():
    database = Database()
    database_column = DatabaseColumn(Config().table, "vin_invalid_length")
    code = VinCode()
    result = database.check_column_values_against_code(database_column, code)
    assert result == False


