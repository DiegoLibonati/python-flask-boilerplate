import pytest
from pydantic import BaseModel
from pymongo.errors import ConnectionFailure

from src.constants.codes import CODE_ERROR_DATABASE, CODE_ERROR_PYDANTIC
from src.utils.exceptions import InternalAPIError, ValidationAPIError
from src.utils.exceptions_handler import exceptions_handler


class _StrictIntModel(BaseModel):
    x: int


def _raise_validation_error() -> None:
    _StrictIntModel(x="not_an_int")  # type: ignore[arg-type]


class TestExceptionsHandler:
    @pytest.mark.unit
    def test_passes_through_return_value(self) -> None:
        @exceptions_handler
        def fn() -> str:
            return "ok"

        result: str = fn()
        assert result == "ok"

    @pytest.mark.unit
    def test_catches_pydantic_validation_error_and_raises_validation_api_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            _raise_validation_error()

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()
        assert exc_info.value.code == CODE_ERROR_PYDANTIC
        assert exc_info.value.status_code == 400

    @pytest.mark.unit
    def test_catches_pymongo_error_and_raises_internal_api_error(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise ConnectionFailure("connection failed")

        with pytest.raises(InternalAPIError) as exc_info:
            fn()
        assert exc_info.value.code == CODE_ERROR_DATABASE
        assert exc_info.value.status_code == 500

    @pytest.mark.unit
    def test_preserves_function_name_via_wraps(self) -> None:
        @exceptions_handler
        def my_named_function() -> None:
            pass

        assert my_named_function.__name__ == "my_named_function"

    @pytest.mark.unit
    def test_passes_args_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(a: int, b: int) -> int:
            return a + b

        result: int = fn(2, 3)
        assert result == 5

    @pytest.mark.unit
    def test_passes_kwargs_to_wrapped_function(self) -> None:
        @exceptions_handler
        def fn(name: str = "") -> str:
            return f"hello {name}"

        result: str = fn(name="world")
        assert result == "hello world"

    @pytest.mark.unit
    def test_does_not_catch_unrelated_exceptions(self) -> None:
        @exceptions_handler
        def fn() -> None:
            raise ValueError("unhandled")

        with pytest.raises(ValueError, match="unhandled"):
            fn()

    @pytest.mark.unit
    def test_validation_error_payload_contains_details(self) -> None:
        @exceptions_handler
        def fn() -> None:
            _raise_validation_error()

        with pytest.raises(ValidationAPIError) as exc_info:
            fn()
        assert "details" in exc_info.value.payload
