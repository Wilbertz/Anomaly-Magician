import os
from pathlib import Path
import pytest
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

def test_get_statistics():
    database = Database()
    database.get_statistics()