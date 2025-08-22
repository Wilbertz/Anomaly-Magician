import random
import re

import exrex
from typing import List
from pydantic import BaseModel, Field
from pydantic.v1 import PositiveInt


class CodeModel(BaseModel):
    """
    The base class for all code models.
    """
    name: str = Field(title="Name",
                       description="The human readable name of the code",
                       examples=["ICD-10", "VIN", "IBAN"])
    industries: List[str] | None = Field(default = None, title="Industries",
                            description="The industries where this code is used.")
    iso_code: str | None = Field(default=None, title="ISO Code",
                           description="The name of the ISO standard in case an ISO code is used.")
    fixed_length: int | None = Field(default=None, title="Fixed Length",
                                     description="The fixed number of characters all code instances must have.")
    min_length: int = Field(default_factory=lambda data: data['fixed_length'], title="Minimum Length",
                            description="The minimum number of characters a code must have.")
    max_length: int = Field(default_factory=lambda data: data['fixed_length'], title="Maximum Length",
                            description="The maximum number of characters a code can have.")
    regex: re.Pattern | None = Field(default=None, title="Regular Expression",
                                     description="A regular expression used to validate the code.")
    values: list[str] | None = Field(default=None, title="Value list",
                                     description="A complete list of possible values.")

    def simple_check(self, code: str)  -> bool:
        """
        A quick and fast way to check if the code is syntactically correct.
        No check is attempted to check whether an instance of the object
        identified by this code really exists.
        :return: A boolean indicating whether the code is syntactically correct.
        """
        pass

    def complex_check(self, code: str) -> bool:
        """
        A time-consuming and potentially expansive way to check both whether
        the code is syntactically correct and whether an instance of the object
        really exists in the real world. Typically, an external service is called.
        :return: A boolean indicating whether the code is syntactically correct.
        """
        pass

    def create_sample_codes(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes.
        :param count: The number of codes to create.
        :return: The list of sample codes.
        """
        pass

    def _create_sample_codes_from_values(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes based
        on the value list.
        :param count: The number of codes to create.
        :return: The list of sample codes.
        """
        if self.values is None or len(self.values) == 0:
            raise ValueError("Must specify a value list.")
        else:
            return random.choices(self.values, k=count)

    def _create_sample_codes_from_regex(self, count: PositiveInt) -> list[str]:
        """
        A quick and fast way to create syntactically correct sample codes based
        on the regular expression.
        :param count: The number of codes to create.
        :return: The list of sample codes.
        """
        if self.regex is None:
            raise ValueError("Must specify a regular expression.")
        else:
            return [exrex.getone(self.regex.pattern) for _ in range(count)]

