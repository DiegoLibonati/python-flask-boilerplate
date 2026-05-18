import pytest
from pydantic import BaseModel

from src.constants.codes import CODE_ERROR_INTERNAL_SERVER, CODE_ERROR_PYDANTIC
from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_decorator import exceptions_decorator


class _DummyModel(BaseModel):
    value: int


@exceptions_decorator
def _raise_pydantic_error() -> None:
    _DummyModel(value="not-an-int")  # type: ignore[arg-type]


@exceptions_decorator
def _passthrough(x: int) -> int:
    return x


@exceptions_decorator
def _raise_runtime_error() -> None:
    raise RuntimeError("oops")


@exceptions_decorator
def _named_function() -> int:
    return 42


@pytest.mark.unit
class TestExceptionsDecorator:
    def test_calls_through_when_no_exception(self) -> None:
        result: int = _passthrough(42)

        assert result == 42

    def test_converts_pydantic_validation_error_to_validation_api_error(self) -> None:
        with pytest.raises(ValidationAPIError):
            _raise_pydantic_error()

    def test_converted_error_has_pydantic_code(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _raise_pydantic_error()

        assert exc_info.value.code == CODE_ERROR_PYDANTIC

    def test_converted_error_has_400_status_code(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _raise_pydantic_error()

        assert exc_info.value.status_code == 400

    def test_converted_error_payload_contains_details(self) -> None:
        with pytest.raises(ValidationAPIError) as exc_info:
            _raise_pydantic_error()

        assert "details" in exc_info.value.payload

    def test_unexpected_errors_are_converted_to_internal_api_error(self) -> None:
        with pytest.raises(InternalAPIError) as exc_info:
            _raise_runtime_error()

        assert exc_info.value.code == CODE_ERROR_INTERNAL_SERVER
        assert exc_info.value.status_code == 500
        assert isinstance(exc_info.value.__cause__, RuntimeError)

    def test_preserves_wrapped_function_name(self) -> None:
        assert _named_function.__name__ == "_named_function"
