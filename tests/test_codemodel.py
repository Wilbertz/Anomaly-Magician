from codes.CodeModel import CodeModel


def test_dummy():
    assert 1 == 1

def test_get_all_code_classes():
    code_classes = CodeModel.get_all_code_classes()
    assert code_classes
