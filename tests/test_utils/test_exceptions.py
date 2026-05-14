from typing import Any

import pytest
from flask import Flask

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
    def test_is_exception_subclass(self) -> None:
        assert issubclass(BaseAPIError, Exception)

    def test_default_status_code_is_500(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.status_code == 500

    def test_default_message_is_set(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.message == "Internal server error."

    def test_custom_message_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(message="custom message")

        assert error.message == "custom message"

    def test_custom_status_code_overrides_default(self) -> None:
        error: BaseAPIError = BaseAPIError(status_code=418)

        assert error.status_code == 418

    def test_custom_code_is_stored(self) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE")

        assert error.code == "MY_CODE"

    def test_payload_defaults_to_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError()

        assert error.payload == {}

    def test_custom_payload_is_stored(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"key": "value"})

        assert error.payload == {"key": "value"}

    def test_none_payload_becomes_empty_dict(self) -> None:
        error: BaseAPIError = BaseAPIError(payload=None)

        assert error.payload == {}


@pytest.mark.unit
class TestBaseAPIErrorToDict:
    def test_includes_code_and_message(self) -> None:
        error: BaseAPIError = BaseAPIError(code="MY_CODE", message="my message")

        result: dict[str, Any] = error.to_dict()

        assert result["code"] == "MY_CODE"
        assert result["message"] == "my message"

    def test_excludes_payload_when_empty(self) -> None:
        error: BaseAPIError = BaseAPIError()

        result: dict[str, Any] = error.to_dict()

        assert "payload" not in result

    def test_includes_payload_when_present(self) -> None:
        error: BaseAPIError = BaseAPIError(payload={"detail": "info"})

        result: dict[str, Any] = error.to_dict()

        assert "payload" in result
        assert result["payload"] == {"detail": "info"}


@pytest.mark.unit
class TestBaseAPIErrorFlaskResponse:
    def test_returns_correct_status_code(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(status_code=418)
            _, status = error.flask_response()

        assert status == 418

    def test_response_body_contains_code(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(code="MY_CODE", message="msg")
            response_obj, _ = error.flask_response()

        assert response_obj.get_json()["code"] == "MY_CODE"

    def test_response_body_contains_message(self, app: Flask) -> None:
        with app.app_context():
            error: BaseAPIError = BaseAPIError(code="X", message="my message")
            response_obj, _ = error.flask_response()

        assert response_obj.get_json()["message"] == "my message"


@pytest.mark.unit
class TestValidationAPIError:
    def test_status_code_is_400(self) -> None:
        assert ValidationAPIError.status_code == 400

    def test_inherits_from_base(self) -> None:
        assert issubclass(ValidationAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: ValidationAPIError = ValidationAPIError()

        assert error.status_code == 400


@pytest.mark.unit
class TestAuthenticationAPIError:
    def test_status_code_is_401(self) -> None:
        assert AuthenticationAPIError.status_code == 401

    def test_inherits_from_base(self) -> None:
        assert issubclass(AuthenticationAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: AuthenticationAPIError = AuthenticationAPIError()

        assert error.status_code == 401


@pytest.mark.unit
class TestNotFoundAPIError:
    def test_status_code_is_404(self) -> None:
        assert NotFoundAPIError.status_code == 404

    def test_inherits_from_base(self) -> None:
        assert issubclass(NotFoundAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: NotFoundAPIError = NotFoundAPIError()

        assert error.status_code == 404


@pytest.mark.unit
class TestConflictAPIError:
    def test_status_code_is_409(self) -> None:
        assert ConflictAPIError.status_code == 409

    def test_inherits_from_base(self) -> None:
        assert issubclass(ConflictAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: ConflictAPIError = ConflictAPIError()

        assert error.status_code == 409


@pytest.mark.unit
class TestBusinessAPIError:
    def test_status_code_is_422(self) -> None:
        assert BusinessAPIError.status_code == 422

    def test_inherits_from_base(self) -> None:
        assert issubclass(BusinessAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: BusinessAPIError = BusinessAPIError()

        assert error.status_code == 422


@pytest.mark.unit
class TestInternalAPIError:
    def test_status_code_is_500(self) -> None:
        assert InternalAPIError.status_code == 500

    def test_inherits_from_base(self) -> None:
        assert issubclass(InternalAPIError, BaseAPIError)

    def test_instance_has_correct_status_code(self) -> None:
        error: InternalAPIError = InternalAPIError()

        assert error.status_code == 500
