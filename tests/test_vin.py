from codes.VinCode import VinCode


def test_dummy():
    assert 1 == 1

def test_create_instance():
    vin_code = VinCode()

    assert vin_code is not None
    assert vin_code.name == "VIN"
    assert vin_code.industries == ["Manufacturing"]
    assert vin_code.iso_code == "ISO-3779"
    assert vin_code.fixed_length == 17
    assert vin_code.min_length == 17
    assert vin_code.max_length == 17
    assert vin_code.regex # No check for specific regex.
    assert vin_code.values is None

def test_simple_check():
    vin_code = VinCode()
    result =  vin_code.simple_check("V58XFC7M8L7PVBND5")
    assert result

def test_create_sample_codes():
    vin_code = VinCode()
    sample_codes = vin_code.create_sample_codes(10)
    assert len(sample_codes) == 10

def test_create_sample_codes_from_regex():
    vin_code = VinCode()
    sample_codes = vin_code._create_sample_codes_from_regex(10)
    assert sample_codes
    assert len(sample_codes) == 10

def test_compute_check_digits():
    vin_code = VinCode()
    result = vin_code._compute_check_digits("VL1UA89ZC6UMSKDN6")
    assert result
    assert result == '6'

