import pytest
from pydantic import BaseModel

from src.constants.codes import CODE_ERROR_PYDANTIC
from src.utils.exceptions import ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


class _DummyModel(BaseModel):
    name: str


@exceptions_handler
def _controller_missing_field() -> None:
    _DummyModel()


@exceptions_handler
def _controller_returns_value() -> str:
    return "ok"


@exceptions_handler
def _controller_raises_value_error() -> None:
    raise ValueError("unexpected error")


@pytest.mark.unit
class TestExceptionsHandler:
    def test_wraps_pydantic_validation_error_as_validation_api_error(self) -> None:
        with pytest.raises(ValidationAPIError):
            _controller_missing_field()

    def test_validation_api_error_has_pydantic_code(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _controller_missing_field()
        assert exc_info.value.code == CODE_ERROR_PYDANTIC

    def test_validation_api_error_has_400_status_code(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _controller_missing_field()
        assert exc_info.value.status_code == 400

    def test_validation_api_error_payload_contains_details(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _controller_missing_field()
        assert "details" in exc_info.value.payload

    def test_returns_value_when_no_error_is_raised(self) -> None:
        result: str = _controller_returns_value()
        assert result == "ok"

    def test_non_pydantic_exceptions_propagate_unchanged(self) -> None:
        with pytest.raises(ValueError, match="unexpected error"):
            _controller_raises_value_error()

    def test_preserves_wrapped_function_name(self) -> None:
        assert _controller_returns_value.__name__ == "_controller_returns_value"
