import pytest
from pydantic import ValidationError

from src.models.template_model import TemplateModel


class TestTemplateModel:
    @pytest.mark.unit
    def test_creates_model_with_valid_name(self) -> None:
        model: TemplateModel = TemplateModel(name="valid_name")
        assert model.name == "valid_name"

    @pytest.mark.unit
    def test_strips_whitespace_from_name(self) -> None:
        model: TemplateModel = TemplateModel(name="  spaced  ")
        assert model.name == "spaced"

    @pytest.mark.unit
    def test_raises_validation_error_for_empty_string(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="")

    @pytest.mark.unit
    def test_raises_validation_error_for_whitespace_only(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel(name="   ")

    @pytest.mark.unit
    def test_raises_validation_error_when_name_missing(self) -> None:
        with pytest.raises(ValidationError):
            TemplateModel()

    @pytest.mark.unit
    def test_model_dump_returns_dict(self) -> None:
        model: TemplateModel = TemplateModel(name="dump_test")
        result: dict[str, str] = model.model_dump()
        assert result == {"name": "dump_test"}

    @pytest.mark.unit
    def test_name_is_string(self) -> None:
        model: TemplateModel = TemplateModel(name="string_check")
        assert isinstance(model.name, str)
