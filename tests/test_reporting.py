import os
from pathlib import Path

import pytest

from database.reporting import Reporting

@pytest.fixture(autouse=True)
def run_before_tests(monkeypatch):
    monkeypatch.chdir(Path(os.getcwd()).parent)

def test_dummy():
    assert 1 == 1

def test_report():
    reporting = Reporting()
    reporting.report()