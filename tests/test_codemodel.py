from codes.CodeModel import CodeModel
from codes.VinCode import VinCode


def test_dummy():
    assert 1 == 1

def test_get_all_code_classes():
    blubber = VinCode()
    code_classes = CodeModel.get_all_code_classes()

    print(code_classes)
