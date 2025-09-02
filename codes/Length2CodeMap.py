class Length2CodeMap:
    """
    This class (implemented as a singleton) maps code lengths to codes.
    """
    _instance = None

    _codes_map: dict[int, str] | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def __init__(self):
        _codes_map = {
            17: "VinCode"
        }

    def get_code(self, code_length: int) -> any:
        if code_length in self._codes_map:
            return globals()[self._codes_map[code_length]]
        return None

