import re
import pytest

from pydantic import ValidationError
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

    @pytest.mark.parametrize(
        "fixed_length",
        [1, 10, 17, 34, 100],
    )
    def test_min_max_length_default_to_fixed_length(self, fixed_length):
        """Test that min/max length inherit fixed_length."""
        model = TestableCodeModel(
            name="Test",
            fixed_length=fixed_length,
        )

        assert model.min_length == fixed_length
        assert model.max_length == fixed_length

    def test_min_max_length_without_fixed_length(self):
        """Test that min/max length default to None."""
        model = TestableCodeModel(name="Test")

        assert model.fixed_length is None
        assert model.min_length is None
        assert model.max_length is None

    def test_explicit_min_max_length(self):
        """Test explicitly specified minimum and maximum lengths."""
        model = TestableCodeModel(
            name="Test",
            min_length=5,
            max_length=20,
        )

        assert model.min_length == 5
        assert model.max_length == 20

    def test_explicit_lengths_match_fixed_length(self):
        """Test that explicit lengths matching fixed_length are accepted."""

        model = TestableCodeModel(
            name="Test",
            fixed_length=17,
            min_length=17,
            max_length=17,
        )

        assert model.fixed_length == 17
        assert model.min_length == 17
        assert model.max_length == 17

    @pytest.mark.parametrize(
        "min_length,max_length",
        [
            (10, 17),
            (17, 20),
            (10, 20),
        ],
    )
    def test_conflicting_lengths(self, min_length, max_length):
        """Test that lengths conflicting with fixed_length are rejected."""

        with pytest.raises(ValidationError):
            TestableCodeModel(
                name="Test",
                fixed_length=17,
                min_length=min_length,
                max_length=max_length,
            )

    @pytest.mark.parametrize(
        "field,value",
        [
            ("min_length", "invalid"),
            ("max_length", "invalid"),
            ("industries", "Automotive"),
            ("values", "ABC"),
            ("iso_code", 123),
        ],
    )
    def test_invalid_field_types(self, field, value):
        """Test validation of incorrect field types."""
        with pytest.raises(ValidationError):
            TestableCodeModel(
                name="Test",
                **{field: value},
            )