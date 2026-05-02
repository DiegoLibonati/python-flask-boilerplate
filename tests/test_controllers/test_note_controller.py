from typing import Any
from unittest.mock import patch

import pytest

from src.constants.codes import CODE_ALREADY_EXISTS_NOTE, CODE_NOT_FOUND_NOTE, CODE_SUCCESS_ADD_NOTE, CODE_SUCCESS_DELETE_NOTE, CODE_SUCCESS_GET_NOTES
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_NOTE,
    MESSAGE_NOT_FOUND_NOTE,
    MESSAGE_SUCCESS_ADD_NOTE,
    MESSAGE_SUCCESS_DELETE_NOTE,
    MESSAGE_SUCCESS_GET_NOTES,
)
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


@pytest.mark.integration
class TestAliveController:
    def test_response_contains_all_expected_keys(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        data: dict[str, str] = response.get_json()
        assert "message" in data
        assert "version_bp" in data
        assert "author" in data
        assert "name_bp" in data

    def test_status_code_is_200(self, client) -> None:
        response = client.get("/api/v1/notes/alive")
        assert response.status_code == 200


@pytest.mark.integration
class TestCreateNoteController:
    def test_response_contains_code_message_data(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "1", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        data: dict[str, Any] = response.get_json()
        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_response_code_matches_constant(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "1", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_ADD_NOTE

    def test_response_message_matches_constant(self, client) -> None:
        mock_note: dict[str, Any] = {"_id": "1", "name": "test", "created_at": "2024-01-01"}
        with patch("src.controllers.note_controller.NoteService.add_note", return_value=mock_note):
            response = client.post("/api/v1/notes/", json={"name": "test"})
        data: dict[str, Any] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_ADD_NOTE

    def test_validation_error_response_has_code_and_message(self, client) -> None:
        response = client.post("/api/v1/notes/", json={"name": ""})
        data: dict[str, Any] = response.get_json()
        assert "code" in data
        assert "message" in data

    def test_conflict_error_response_has_correct_code(self, client) -> None:
        with patch(
            "src.controllers.note_controller.NoteService.add_note",
            side_effect=ConflictAPIError(code=CODE_ALREADY_EXISTS_NOTE, message=MESSAGE_ALREADY_EXISTS_NOTE),
        ):
            response = client.post("/api/v1/notes/", json={"name": "existing"})
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_ALREADY_EXISTS_NOTE


@pytest.mark.integration
class TestGetNotesController:
    def test_response_contains_code_message_data(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert "code" in data
        assert "message" in data
        assert "data" in data

    def test_response_code_matches_constant(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["code"] == CODE_SUCCESS_GET_NOTES

    def test_response_message_matches_constant(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.get_all_notes", return_value=[]):
            response = client.get("/api/v1/notes/")
        data: dict[str, Any] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_GET_NOTES


@pytest.mark.integration
class TestDeleteNoteController:
    def test_response_contains_code_and_message(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.delete_note_by_id", return_value=True):
            response = client.delete("/api/v1/notes/some-id")
        data: dict[str, str] = response.get_json()
        assert "code" in data
        assert "message" in data

    def test_response_code_matches_constant(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.delete_note_by_id", return_value=True):
            response = client.delete("/api/v1/notes/some-id")
        data: dict[str, str] = response.get_json()
        assert data["code"] == CODE_SUCCESS_DELETE_NOTE

    def test_response_message_matches_constant(self, client) -> None:
        with patch("src.controllers.note_controller.NoteService.delete_note_by_id", return_value=True):
            response = client.delete("/api/v1/notes/some-id")
        data: dict[str, str] = response.get_json()
        assert data["message"] == MESSAGE_SUCCESS_DELETE_NOTE

    def test_not_found_response_has_correct_code(self, client) -> None:
        with patch(
            "src.controllers.note_controller.NoteService.delete_note_by_id",
            side_effect=NotFoundAPIError(code=CODE_NOT_FOUND_NOTE, message=MESSAGE_NOT_FOUND_NOTE),
        ):
            response = client.delete("/api/v1/notes/nonexistent")
        data: dict[str, str] = response.get_json()
        assert data["code"] == CODE_NOT_FOUND_NOTE
