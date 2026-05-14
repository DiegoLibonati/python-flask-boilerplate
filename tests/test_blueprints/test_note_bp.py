from typing import Any
from unittest.mock import patch

import pytest

from src.constants.codes import (
    CODE_ALREADY_EXISTS_NOTE,
    CODE_NOT_FOUND_NOTE,
    CODE_SUCCESS_ADD_NOTE,
    CODE_SUCCESS_DELETE_NOTE,
    CODE_SUCCESS_GET_NOTES,
)
from src.constants.messages import MESSAGE_ALREADY_EXISTS_NOTE, MESSAGE_NOT_FOUND_NOTE
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


@pytest.mark.integration
class TestAliveRoute:
    def test_returns_200(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        assert response.status_code == 200

    def test_response_has_message(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, str] = response.get_json()
        assert data["message"] == "I am Alive!"

    def test_response_has_version_and_author(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, str] = response.get_json()
        assert data["version_bp"] == "1.0.0"
        assert data["author"] == "Diego Libonati"

    def test_response_has_name_bp(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, str] = response.get_json()
        assert data["name_bp"] == "Note"

    def test_post_method_not_allowed(self, client) -> None:
        response = client.post("/api/v1/notes/alive")
        assert response.status_code == 405


@pytest.mark.integration
class TestTestErrorRoute:
    def test_returns_500(self, client) -> None:
        response = client.get("/api/v1/notes/test_error")
        assert response.status_code == 500

    def test_response_has_code_and_message(self, client) -> None:
        response = client.get("/api/v1/notes/test_error")
        data: dict[str, str] = response.get_json()
        assert "code" in data
        assert "message" in data


@pytest.mark.integration
class TestCreateNoteRoute:
    def test_returns_201_with_valid_body(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "abc", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        assert response.status_code == 201

    def test_response_has_success_code(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "abc", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_ADD_NOTE

    def test_response_has_data(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "abc", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        data: dict[str, Any] = response.get_json()
        assert data["data"] == mock_note

    def test_returns_400_with_empty_name(self, client) -> None:
        response = client.post("/api/v1/notes/", json={"name": ""})
        assert response.status_code == 400

    def test_returns_400_with_missing_name(self, client) -> None:
        response = client.post("/api/v1/notes/", json={})
        assert response.status_code == 400

    def test_returns_400_with_whitespace_only_name(self, client) -> None:
        response = client.post("/api/v1/notes/", json={"name": "   "})
        assert response.status_code == 400

    def test_returns_409_when_note_already_exists(self, client) -> None:
        with patch(
            "src.controllers.note_controller.NoteService.add_note",
            side_effect=ConflictAPIError(code=CODE_ALREADY_EXISTS_NOTE, message=MESSAGE_ALREADY_EXISTS_NOTE),
        ):
            response = client.post("/api/v1/notes/", json={"name": "existing"})
        assert response.status_code == 409


@pytest.mark.integration
class TestGetNotesRoute:
    def test_returns_200(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        assert response.status_code == 200

    def test_response_has_success_code(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_GET_NOTES

    def test_response_data_is_list(self, client) -> None:
        mock_notes: list[dict[str, Any]] = [{"_id": "1", "name": "hi"}]
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=mock_notes):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert isinstance(data["data"], list)

    def test_response_data_matches_service_result(self, client) -> None:
        mock_notes: list[dict[str, Any]] = [{"_id": "1", "name": "hi"}]
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=mock_notes):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["data"] == mock_notes


@pytest.mark.integration
class TestDeleteNoteRoute:
    def test_returns_200_when_note_exists(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.delete_note_by_id", return_value=True):
            response = client.delete("/api/v1/notes/some-id")
        assert response.status_code == 200

    def test_response_has_success_code(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.delete_note_by_id", return_value=True):
            response = client.delete("/api/v1/notes/some-id")
        data: dict[str, str] = response.get_json()
        assert data["code"] == CODE_SUCCESS_DELETE_NOTE

    def test_returns_404_when_note_not_found(self, client) -> None:
        with patch(
            "src.controllers.note_controller.NoteService.delete_note_by_id",
            side_effect=NotFoundAPIError(code=CODE_NOT_FOUND_NOTE, message=MESSAGE_NOT_FOUND_NOTE),
        ):
            response = client.delete("/api/v1/notes/nonexistent")
        assert response.status_code == 404

    def test_get_method_not_allowed_on_delete_endpoint(self, client) -> None:
        response = client.get("/api/v1/notes/some-id")
        assert response.status_code == 405
