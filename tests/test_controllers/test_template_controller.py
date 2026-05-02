from typing import Any

import pytest
from flask import Flask

from src.controllers.template_controller import alive
from src.controllers.template_controller import test_error as controller_test_error
from src.utils.exceptions import InternalAPIError


class TestAliveController:
    @pytest.mark.unit
    def test_returns_tuple_with_200_status(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
        assert status == 200

    @pytest.mark.unit
    def test_response_json_has_message(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    @pytest.mark.unit
    def test_response_json_has_version_bp(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["version_bp"] == "1.0.0"

    @pytest.mark.unit
    def test_response_json_has_author(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["author"] == "Diego Libonati"

    @pytest.mark.unit
    def test_response_json_has_name_bp(self, app: Flask) -> None:
        with app.app_context():
            response, status = alive()
            data: dict[str, Any] = response.get_json()
        assert data["name_bp"] == "Template"


class TestTestErrorController:
    @pytest.mark.unit
    def test_raises_internal_api_error(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError):
                controller_test_error()

    @pytest.mark.unit
    def test_error_has_correct_code(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.code == "CODE_TEMPLATE_ERROR_TEST_MESSAGE"

    @pytest.mark.unit
    def test_error_has_correct_message(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.message == "TemplateError test message."

    @pytest.mark.unit
    def test_error_has_500_status_code(self, app: Flask) -> None:
        with app.app_context():
            with pytest.raises(InternalAPIError) as exc_info:
                controller_test_error()
        assert exc_info.value.status_code == 500
