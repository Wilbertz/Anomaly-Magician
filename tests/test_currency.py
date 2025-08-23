from codes.CurrencyCode import CurrencyCode

def test_dummy():
    assert 1 == 1

def test_create_instance():
    currency_code = CurrencyCode()

    assert currency_code is not None
    assert currency_code.name == "Currency"
    assert currency_code.industries == ["Finance"]
    assert currency_code.iso_code == "ISO-4217"
    assert currency_code.fixed_length == 3
    assert currency_code.min_length == 3
    assert currency_code.max_length == 3
    assert currency_code.regex is None
    assert len(currency_code.values) == 179

def test_simple_check():
    currency_code = CurrencyCode()
    result =  currency_code.simple_check("EUR")
    assert result

def test_create_sample_codes():
    currency_code = CurrencyCode()
    sample_codes = currency_code.create_sample_codes(10)
    assert len(sample_codes) == 10