from codes.Icd10Code import Icd10Code


def test_dummy():
    assert 1 == 1

def test_create_instance():
    icd_10_code = Icd10Code()

    assert icd_10_code is not None
    assert icd_10_code.name == "ICD-10"
    assert icd_10_code.industries == ["Healthcare"]
    assert icd_10_code.iso_code is None
    assert icd_10_code.fixed_length is None
    assert icd_10_code.min_length == 3
    assert icd_10_code.max_length == 7
    assert icd_10_code.regex is not None # No check for specific regex.
    assert icd_10_code.values is None

