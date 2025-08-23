import re

from pydantic.v1 import PositiveInt

from codes.CodeModel import CodeModel


class Icd10Code(CodeModel):
    """
    ICD-10 is the 10th revision of the International Classification of Diseases (ICD),
    a medical classification list by the World Health Organization (WHO).
    It contains codes for diseases, signs and symptoms, abnormal findings, complaints,
    social circumstances, and external causes of injury or diseases.
    """

    def __init__(self):
        super().__init__()
        self.name = "ICD-10"
        self.industries = ["Healthcare"]
        self.iso_code = None
        self.fixed_length = None
        self.min_length = 3
        self.max_length = 7 # WHO-ICD-10 has a maximum of 6 characters.
        self.regex = re.compile(r"^[A-Z][0-9]{2}(?:\.[A-Z0-9]{1,4})?$")

    def simple_check(self, code: str) -> bool:
        pass

    def complex_check(self, code: str) -> bool:
        pass

    def create_sample_codes(self, count: PositiveInt) -> list[str]:
        pass