from typing import Any

import pytest

from src.constants.codes import CODE_ERROR_INTERNAL_SERVER
from src.constants.messages import MESSAGE_ERROR_INTERNAL_SERVER
from src.utils.exceptions import (
    AuthenticationAPIError,
    BaseAPIError,
    BusinessAPIError,
    ConflictAPIError,
    InternalAPIError,
    NotFoundAPIError,
    ValidationAPIError,
)


class TestBaseAPIError:
    @pytest.mark.unit
    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.status_code == 500

    @pytest.mark.unit
    def test_default_message_is_internal_server(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.message == MESSAGE_ERROR_INTERNAL_SERVER

    @pytest.mark.unit
    def test_default_code_is_internal_server(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.code == CODE_ERROR_INTERNAL_SERVER

    @pytest.mark.unit
    def test_custom_message_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(code="X", message="custom message")
        assert error.message == "custom message"

    @pytest.mark.unit
    def test_custom_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE")
        assert error.code == "MY_CODE"

    @pytest.mark.unit
    def test_custom_status_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(code="X", status_code=418)
        assert error.status_code == 418

    @pytest.mark.unit
    def test_payload_defaults_to_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.payload == {}

    @pytest.mark.unit
    def test_payload_stored_when_provided(self) -> None:
        payload: dict[str, Any] = {"key": "value"}
        error: BaseAPIError = BaseAPIError(code="X", payload=payload)
        assert error.payload == payload

    @pytest.mark.unit
    def test_to_dict_returns_code_and_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="TEST_CODE", message="test msg")
        result: dict[str, Any] = error.to_dict()
        assert result["code"] == "TEST_CODE"
        assert result["message"] == "test msg"

    @pytest.mark.unit
    def test_to_dict_excludes_payload_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError(code="X")
        result: dict[str, Any] = error.to_dict()
        assert "payload" not in result

    @pytest.mark.unit
    def test_to_dict_includes_payload_when_set(self) -> None:
        error: BaseAPIError = BaseAPIError(code="X", payload={"detail": "info"})
        result: dict[str, Any] = error.to_dict()
        assert "payload" in result
        assert result["payload"]["detail"] == "info"

    @pytest.mark.unit
    def test_is_exception(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert isinstance(error, Exception)


class TestValidationAPIError:
    @pytest.mark.unit
    def test_status_code_is_400(self) -> None:
        error: ValidationAPIError = ValidationAPIError(code="X")
        assert error.status_code == 400


class TestAuthenticationAPIError:
    @pytest.mark.unit
    def test_status_code_is_401(self) -> None:
        error: AuthenticationAPIError = AuthenticationAPIError(code="X")
        assert error.status_code == 401


class TestNotFoundAPIError:
    @pytest.mark.unit
    def test_status_code_is_404(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError(code="X")
        assert error.status_code == 404


class TestConflictAPIError:
    @pytest.mark.unit
    def test_status_code_is_409(self) -> None:
        error: ConflictAPIError = ConflictAPIError(code="X")
        assert error.status_code == 409


class TestBusinessAPIError:
    @pytest.mark.unit
    def test_status_code_is_422(self) -> None:
        error: BusinessAPIError = BusinessAPIError(code="X")
        assert error.status_code == 422


class TestInternalAPIError:
    @pytest.mark.unit
    def test_status_code_is_500(self) -> None:
        error: InternalAPIError = InternalAPIError(code="X")
        assert error.status_code == 500
