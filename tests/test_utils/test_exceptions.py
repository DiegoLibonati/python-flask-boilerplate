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


@pytest.mark.unit
class TestBaseAPIError:
    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.status_code == 500

    def test_default_message_is_internal_server_error(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.message == MESSAGE_ERROR_INTERNAL_SERVER

    def test_default_code_is_internal_server_error(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.code == CODE_ERROR_INTERNAL_SERVER

    def test_custom_message_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom message")
        assert error.message == "custom message"

    def test_custom_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(code="CUSTOM_CODE")
        assert error.code == "CUSTOM_CODE"

    def test_custom_status_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)
        assert error.status_code == 418

    def test_payload_defaults_to_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError()
        assert error.payload == {}

    def test_payload_is_stored_when_provided(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"key": "value"})
        assert error.payload == {"key": "value"}

    def test_is_exception_subclass(self) -> None:
        assert isinstance(BaseAPIError(), Exception)

    def test_to_dict_contains_code(self) -> None:
        error: BaseAPIError = BaseAPIError(code="TEST_CODE")
        result: dict[str, Any] = error.to_dict()
        assert result["code"] == "TEST_CODE"

    def test_to_dict_contains_message(self) -> None:
        error: BaseAPIError = BaseAPIError(message="test message")
        result: dict[str, Any] = error.to_dict()
        assert result["message"] == "test message"

    def test_to_dict_does_not_include_payload_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError()
        result: dict[str, Any] = error.to_dict()
        assert "payload" not in result

    def test_to_dict_includes_payload_when_not_empty(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"detail": "info"})
        result: dict[str, Any] = error.to_dict()
        assert "payload" in result
        assert result["payload"] == {"detail": "info"}

    def test_flask_response_returns_correct_status_code(self, app) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(status_code=500)
            _, status_code = error.flask_response()
        assert status_code == 500

    def test_flask_response_body_contains_code(self, app) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(code="MY_CODE", message="msg")
            response, _ = error.flask_response()
        data: dict[str, str] = response.get_json()
        assert data["code"] == "MY_CODE"


@pytest.mark.unit
class TestValidationAPIError:
    def test_status_code_is_400(self) -> None:
        assert ValidationAPIError().status_code == 400

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(ValidationAPIError, BaseAPIError)

    def test_custom_code_and_message_are_stored(self) -> None:
        error: ValidationAPIError = ValidationAPIError(code="VAL_ERR", message="bad input")
        assert error.code == "VAL_ERR"
        assert error.message == "bad input"


@pytest.mark.unit
class TestAuthenticationAPIError:
    def test_status_code_is_401(self) -> None:
        assert AuthenticationAPIError().status_code == 401

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(AuthenticationAPIError, BaseAPIError)


@pytest.mark.unit
class TestNotFoundAPIError:
    def test_status_code_is_404(self) -> None:
        assert NotFoundAPIError().status_code == 404

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(NotFoundAPIError, BaseAPIError)


@pytest.mark.unit
class TestConflictAPIError:
    def test_status_code_is_409(self) -> None:
        assert ConflictAPIError().status_code == 409

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(ConflictAPIError, BaseAPIError)


@pytest.mark.unit
class TestBusinessAPIError:
    def test_status_code_is_422(self) -> None:
        assert BusinessAPIError().status_code == 422

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(BusinessAPIError, BaseAPIError)


@pytest.mark.unit
class TestInternalAPIError:
    def test_status_code_is_500(self) -> None:
        assert InternalAPIError().status_code == 500

    def test_is_subclass_of_base_api_error(self) -> None:
        assert issubclass(InternalAPIError, BaseAPIError)
