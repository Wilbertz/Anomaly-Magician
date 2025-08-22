import re
from typing import List
from pydantic import Field
from pydantic.v1 import PositiveInt
from codes.CodeModel import CodeModel

VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

VIN_VALUES = {
    **{str(i): i for i in range(10)},  # digits
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}

class VinCode(CodeModel):
    """
    A Vehicle Identification Number (VIN) is used to uniquely
    identify automobiles and other vehicles. The VIN was originally
    described in ISO-3779 in 1977 and last revised in 1983.

    https://vpic.nhtsa.dot.gov/api/
    """
    name: str = Field(default="VIN")
    industries: List[str] = Field(default=["Manufacturing"])
    iso_code: bool = Field(default="ISO-3779")
    fixed_length: int = Field(default=17)
    regex: re.Pattern = Field(default=re.compile(r"^[A-HJ-NPR-Z0-9]{17}$"))

    def simple_check(self, code: str) -> bool:
        if not self.regex.match(code):
            return False

        return code[8] == self._compute_check_digits(code)

    def create_sample_codes(self, count: PositiveInt) -> list[str]:
        return [
            s[:8] + self._compute_check_digits(s) + s[9:]
            for s in super()._create_sample_codes_from_regex(count)
        ]

    def _compute_check_digits(self, code: str) -> str:
        """
        Compute the check digit for a VIN (9th character).
        """
        if not self.regex.match(code):
            raise ValueError(f"Invalid VIN format: {code}, Regex pattern: {self.regex.pattern}")

        total = 0
        for i, char in enumerate(code):
            value = VIN_VALUES.get(char)
            if value is None:
                raise ValueError(f"Invalid character in VIN: {char}")
            weight = VIN_WEIGHTS[i]
            total += value * weight

        remainder = total % 11
        return "X" if remainder == 10 else str(remainder)
