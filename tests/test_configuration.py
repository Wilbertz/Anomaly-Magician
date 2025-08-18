from configuration.config import Config


def test_dummy():
    assert 1 == 1

def test_config_singleton():
    config = Config()
    assert config