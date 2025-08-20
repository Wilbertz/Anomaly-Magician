from pydantic import BaseModel
from pydantic.v1 import PositiveInt


class CodeModel(BaseModel):
    """
    The base class for all code models.
    """
    name: str
    industry: str | None
    iso_code: bool
    min_length: int
    max_length: int
    fixed_length: int | None
    regex: str | None
    values: list[str] | None

    def simple_check(self)  -> bool:
        """
        A quick and fast way to check if the code is syntactically correct.
        No check is attempted to check whether an instance of the object
        identified by this code really exists.
        """
        pass

    def complex_check(self) -> bool:
        """
        A time-consuming and potentially expansive way to check both whether
        the code is syntactically correct and whether an instance of the object
        really exists in the real world. Typically, an external service is called.
        """
        pass

    def create_sample_codes(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes.
        """
        pass

    def _create_sample_codes_from_values(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes based
        on the value list.
        :param count: The number of codes to create.
        :return: The list of sample codes.
        """
        pass

    def _create_sample_codes_from_regex(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes based
        on the regular expression.
        :param count: The number of codes to create.
        :return: The list of sample codes.
        """
        pass
