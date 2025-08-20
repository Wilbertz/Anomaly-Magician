from codes.CodeModel import CodeModel


class CurrencyCode(CodeModel):
    """
    ISO 4217 is a standard published by the International Organization for Standardization (ISO)
    that defines alpha codes and numeric codes for the representation of currencies and provides
    information about the relationships between individual currencies and their minor units.
    """
    def __init__(self, code: str, iso_code: bool = False):
        super().__init__(code, iso_code)
        pass