import builtins
import importlib
from typing import List

from codes.VinCode import VinCode


class Length2CodeMap:
    """
    This class (implemented as a singleton) maps code lengths to codes.
    """
    _instance = None

    _codes_map: dict[int, List ] | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._codes_map = {
            17: [VinCode()]
        }

    def resolve_type(self, type_name: str):
        """
        Convert a string into a Python type/class object.

        Supports:
        - Built-in types: "int", "str", "list", "dict", ...
        - Custom classes in current global scope
        - Fully qualified module paths: "datetime.datetime", "collections.Counter"
        """
        # 1. Check built-in types
        if hasattr(builtins, type_name):
            return getattr(builtins, type_name)

        # 2. Check current global scope (e.g. custom classes)
        if type_name in globals():
            return globals()[type_name]

        # 3. Try to resolve fully qualified module path
        if "." in type_name:
            module_name, class_name = type_name.rsplit(".", 1)
            try:
                module = importlib.import_module(module_name)
                return getattr(module, class_name)
            except (ImportError, AttributeError):
                raise ValueError(f"Cannot resolve type '{type_name}'")

        raise ValueError(f"Unknown type name: {type_name}")


    def get_code(self, code_length: int) -> any:
        if code_length in self._codes_map:
            return self._codes_map[code_length]
        return None

