from typing import Any

import pytest
from flask.testing import FlaskClient


class TestAliveRoute:
    @pytest.mark.integration
    def test_returns_200(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "I am Alive!"

    @pytest.mark.integration
    def test_response_contains_version_bp(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data: dict[str, Any] = response.get_json()
        assert "version_bp" in data
        assert data["version_bp"] == "1.0.0"

    @pytest.mark.integration
    def test_response_contains_author(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data: dict[str, Any] = response.get_json()
        assert data["author"] == "Diego Libonati"

    @pytest.mark.integration
    def test_response_contains_name_bp(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        data: dict[str, Any] = response.get_json()
        assert data["name_bp"] == "Template"

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/alive")
        assert response.content_type == "application/json"


class TestTestErrorRoute:
    @pytest.mark.integration
    def test_returns_500(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        assert response.status_code == 500

    @pytest.mark.integration
    def test_response_contains_code(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == "CODE_TEMPLATE_ERROR_TEST_MESSAGE"

    @pytest.mark.integration
    def test_response_contains_message(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == "TemplateError test message."

    @pytest.mark.integration
    def test_response_is_json(self, client: FlaskClient) -> None:
        response = client.get("/api/v1/templates/test_error")
        assert response.content_type == "application/json"
