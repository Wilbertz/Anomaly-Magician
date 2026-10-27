import re

from pydantic.v1 import PositiveInt
from codes.CodeModel import CodeModel


def test_dummy():
    assert 1 == 1

class TestableCodeModel(CodeModel):

    def complex_check(self, code: str) -> bool:
        pass

    def create_sample_codes(self, count: PositiveInt) -> list[str]:
        pass

    def simple_check(self, code: str) -> bool:
        pass


class TestCodeModel:
    """Unit tests for the TestableCodeModel class."""

    def test_get_all_code_classes(self):
        code_classes = CodeModel.get_all_code_classes()
        assert code_classes

    def test_create_model_with_name(self):
        """Test creating a model with only a name."""
        model = TestableCodeModel(name="VIN")

        assert model.name == "VIN"
        assert model.industries is None
        assert model.iso_code is None
        assert model.fixed_length is None
        assert model.min_length is None
        assert model.max_length is None
        assert model.regex is None
        assert model.values is None

    def test_create_model_with_all_fields(self):
        """Test creating a model with all fields."""
        pattern = re.compile(r"^[A-Z0-9]{17}$")

        model = TestableCodeModel(
            name="VIN",
            industries=["Automotive"],
            iso_code="ISO 3779",
            fixed_length=17,
            min_length=17,
            max_length=17,
            regex=pattern,
            values=["ABC12345678901234"],
        )

        assert model.name == "VIN"
        assert model.industries == ["Automotive"]
        assert model.iso_code == "ISO 3779"
        assert model.fixed_length == 17
        assert model.min_length == 17
        assert model.max_length == 17
        assert model.regex == pattern
        assert model.values == ["ABC12345678901234"]