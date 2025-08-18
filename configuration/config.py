import json


class Config:
    """
    This class (implemented as a singleton) implements access to application configuration.
    """
    _instance = None
    _config: dict = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        try:
            self._config = self._read_config()
            self.server = self._config["database"]["server"]
            self.database = self._config["database"]["database"]
            self.table = self._config["database"]["table"]
            self.column = self._config["database"]["column"]
        except FileNotFoundError:
            raise

    @staticmethod
    def _read_config() -> dict:
        with open(".\configuration\config.json") as f:
            _config = json.load(f)
        return _config

