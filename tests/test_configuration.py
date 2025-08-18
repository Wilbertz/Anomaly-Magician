import os
from pathlib import Path
import pytest
from configuration.config import Config

@pytest.fixture(autouse=True)
def run_before_tests(monkeypatch):
    monkeypatch.chdir(Path(os.getcwd()).parent)

def test_dummy():
    assert 1 == 1

def test_config_singleton():
    config1 = Config()
    assert config1
    config2 = Config()
    assert config1 == config2

def test_config_configuration():
    assert Config().server
    assert Config().server == "DESKTOP-2LMIUA2"