from typing import Any
from unittest.mock import patch

import pytest

from src.constants.codes import CODE_ALREADY_EXISTS_NOTE, CODE_NOT_FOUND_NOTE
from src.models.note_model import NoteModel
from src.services.note_service import NoteService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


@pytest.mark.unit
class TestNoteServiceAddNote:
    def test_returns_inserted_note_when_name_is_unique(self) -> None:
        note: NoteModel = NoteModel(name="unique")
        mock_inserted: dict[str, Any] = {"_id": "1", "name": "unique", "created_at": "2024-01-01"}
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=None),
            patch("src.services.note_service.NoteDAO.insert_one", return_value=mock_inserted),
        ):
            result: dict[str, Any] = NoteService.add_note(note)
        assert result == mock_inserted

    def test_calls_insert_one_with_model_dump(self) -> None:
        note: NoteModel = NoteModel(name="unique")
        mock_inserted: dict[str, Any] = {"_id": "1", "name": "unique", "created_at": "2024-01-01"}
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value=None),
            patch("src.services.note_service.NoteDAO.insert_one", return_value=mock_inserted) as mock_insert,
        ):
            NoteService.add_note(note)
        mock_insert.assert_called_once_with({"name": "unique"})

    def test_raises_conflict_error_when_name_already_exists(self) -> None:
        note: NoteModel = NoteModel(name="existing")
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value={"_id": "1", "name": "existing"}),
            pytest.raises(ConflictAPIError),
        ):
            NoteService.add_note(note)

    def test_conflict_error_has_correct_code(self) -> None:
        note: NoteModel = NoteModel(name="existing")
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value={"name": "existing"}),
            pytest.raises(ConflictAPIError) as exc_info,
        ):
            NoteService.add_note(note)
        assert exc_info.value.code == CODE_ALREADY_EXISTS_NOTE

    def test_conflict_error_has_409_status_code(self) -> None:
        note: NoteModel = NoteModel(name="existing")
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value={"name": "existing"}),
            pytest.raises(ConflictAPIError) as exc_info,
        ):
            NoteService.add_note(note)
        assert exc_info.value.status_code == 409

    def test_does_not_insert_when_name_already_exists(self) -> None:
        note: NoteModel = NoteModel(name="existing")
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_name", return_value={"name": "existing"}),
            patch("src.services.note_service.NoteDAO.insert_one") as mock_insert,
            pytest.raises(ConflictAPIError),
        ):
            NoteService.add_note(note)
        mock_insert.assert_not_called()


@pytest.mark.unit
class TestNoteServiceGetAllNotes:
    def test_returns_list_from_dao(self) -> None:
        expected: list[dict[str, Any]] = [{"_id": "1", "name": "a"}]
        with patch("src.services.note_service.NoteDAO.find", return_value=expected):
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        assert result == expected

    def test_returns_empty_list_when_no_notes(self) -> None:
        with patch("src.services.note_service.NoteDAO.find", return_value=[]):
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        assert result == []

    def test_returns_multiple_notes(self) -> None:
        mock_notes: list[dict[str, Any]] = [{"_id": "1", "name": "a"}, {"_id": "2", "name": "b"}]
        with patch("src.services.note_service.NoteDAO.find", return_value=mock_notes):
            result: list[dict[str, Any]] = NoteService.get_all_notes()
        assert len(result) == 2


@pytest.mark.unit
class TestNoteServiceDeleteNoteById:
    def test_returns_true_when_note_is_deleted(self) -> None:
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value={"_id": "1"}),
            patch("src.services.note_service.NoteDAO.delete_one_by_id", return_value=True),
        ):
            result: bool = NoteService.delete_note_by_id("1")
        assert result is True

    def test_raises_not_found_error_when_note_does_not_exist(self) -> None:
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None),
            pytest.raises(NotFoundAPIError),
        ):
            NoteService.delete_note_by_id("nonexistent")

    def test_not_found_error_has_correct_code(self) -> None:
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None),
            pytest.raises(NotFoundAPIError) as exc_info,
        ):
            NoteService.delete_note_by_id("nonexistent")
        assert exc_info.value.code == CODE_NOT_FOUND_NOTE

    def test_not_found_error_has_404_status_code(self) -> None:
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None),
            pytest.raises(NotFoundAPIError) as exc_info,
        ):
            NoteService.delete_note_by_id("nonexistent")
        assert exc_info.value.status_code == 404

    def test_does_not_call_delete_when_note_not_found(self) -> None:
        with (
            patch("src.services.note_service.NoteDAO.find_one_by_id", return_value=None),
            patch("src.services.note_service.NoteDAO.delete_one_by_id") as mock_delete,
            pytest.raises(NotFoundAPIError),
        ):
            NoteService.delete_note_by_id("nonexistent")
        mock_delete.assert_not_called()
