import re
from dataclasses import Field
from typing import List

from codes.CodeModel import CodeModel


class Icd10Code(CodeModel):
    """
    ICD-10 is the 10th revision of the International Classification of Diseases (ICD),
    a medical classification list by the World Health Organization (WHO).
    It contains codes for diseases, signs and symptoms, abnormal findings, complaints,
    social circumstances, and external causes of injury or diseases.
    """
    name: str = Field(default="Currency")
    industries: List[str] = Field(default=["Healthcare"])
    iso_code: str | None = Field(default=None)
    fixed_length: int = Field(default=3)
    regex: re.Pattern = Field(default=re.compile(r"^[A-Z][0-9]{2}(?:\.[A-Z0-9]{1,4})?$"))