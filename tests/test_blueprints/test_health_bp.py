import pytest

from src.constants.codes import CODE_SUCCESS_HEALTH
from src.constants.messages import MESSAGE_SUCCESS_HEALTH


@pytest.mark.integration
class TestHealthRoute:
    def test_returns_200(self, client) -> None:
        response = client.get("/api/v1/health/")

        assert response.status_code == 200

    def test_response_has_success_code(self, client) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, str] = response.get_json()

        assert data["code"] == CODE_SUCCESS_HEALTH

    def test_response_has_success_message(self, client) -> None:
        response = client.get("/api/v1/health/")
        data: dict[str, str] = response.get_json()

        assert data["message"] == MESSAGE_SUCCESS_HEALTH

    def test_post_method_not_allowed(self, client) -> None:
        response = client.post("/api/v1/health/")

        assert response.status_code == 405
