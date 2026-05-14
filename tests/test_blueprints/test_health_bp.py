import pytest

from src.constants.codes import CODE_SUCCESS_HEALTH, CODE_SUCCESS_READY
from src.constants.messages import MESSAGE_SUCCESS_HEALTH, MESSAGE_SUCCESS_READY


@pytest.mark.integration
class TestHealthRoute:
    def test_returns_200(self, client) -> None:
        response = client.get("/health")

        assert response.status_code == 200

    def test_response_has_success_code(self, client) -> None:
        response = client.get("/health")
        data: dict[str, str] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    def test_response_has_success_message(self, client) -> None:
        response = client.get("/health")
        data: dict[str, str] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH

    def test_post_method_not_allowed(self, client) -> None:
        response = client.post("/health")

        assert response.status_code == 405


@pytest.mark.integration
class TestReadyRoute:
    def test_returns_200(self, client) -> None:
        response = client.get("/ready")

        assert response.status_code == 200

    def test_response_has_success_code(self, client) -> None:
        response = client.get("/ready")
        data: dict[str, str] = response.get_json()

        assert data["code"] == CODE_SUCCESS_READY

    def test_response_has_success_message(self, client) -> None:
        response = client.get("/ready")
        data: dict[str, str] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_READY

    def test_post_method_not_allowed(self, client) -> None:
        response = client.post("/ready")

        assert response.status_code == 405
