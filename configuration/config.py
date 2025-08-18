import json


def _read_config() -> dict:
    with open(".\configuration\config.json") as f:
        _config = json.load(f)
    return _config


class Config:
    """
    This class (implemented as a singleton) implements access to application configuration.
    """
    _instance = None
    _config: dict = None
    _server: str = None
    _database: str = None
    _table: str = None
    _column: str = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        try:
            self._config = _read_config()
            self._server = self._config["database"]["server"]
            print(self._server)
        except FileNotFoundError:
            raise FileNotFoundError()



