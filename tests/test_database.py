import os
from pathlib import Path
import pytest

from configuration.config import Config
from database.database import Database


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

def test_get_average_column_length():
    database = Database()
    average_column_length = database.get_average_column_length(Config().table, Config().column)
    assert average_column_length > 0