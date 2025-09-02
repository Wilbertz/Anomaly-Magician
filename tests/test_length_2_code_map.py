from codes.Length2CodeMap import Length2CodeMap


def test_dummy():
    assert 1 == 1

def test_database_singleton():
    code_map_1 = Length2CodeMap()
    assert code_map_1
    code_map_2 = Length2CodeMap()
    assert code_map_1 is code_map_2

def test_can_get_vin_code():
    code_map = Length2CodeMap()
    codes = code_map.get_code(17)

    assert len(codes) == 1

    code_type = type(codes[0])
    print(code_type)