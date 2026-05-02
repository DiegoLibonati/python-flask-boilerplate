from unittest.mock import patch

import pytest

from src.constants.defaults import DEFAULT_NOTES
from src.startup.init_notes import add_default_notes


@pytest.mark.unit
class TestAddDefaultNotes:
    def test_does_not_add_notes_when_store_is_not_empty(self) -> None:
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[{"name": "existing"}]),
            patch("src.startup.init_notes.NoteService.add_note") as mock_add,
        ):
            add_default_notes()
        mock_add.assert_not_called()

    def test_adds_default_notes_when_store_is_empty(self) -> None:
        with patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[]), patch("src.startup.init_notes.NoteService.add_note") as mock_add:
            add_default_notes()
        assert mock_add.call_count == len(DEFAULT_NOTES)

    def test_adds_exactly_two_default_notes(self) -> None:
        with patch("src.startup.init_notes.NoteService.get_all_notes", return_value=[]), patch("src.startup.init_notes.NoteService.add_note") as mock_add:
            add_default_notes()
        assert mock_add.call_count == 2

    def test_returns_early_without_calling_add_when_notes_exist(self) -> None:
        existing_notes: list[dict[str, str]] = [{"name": "hi"}, {"name": "im Die"}]
        with (
            patch("src.startup.init_notes.NoteService.get_all_notes", return_value=existing_notes),
            patch("src.startup.init_notes.NoteService.add_note") as mock_add,
        ):
            add_default_notes()
        mock_add.assert_not_called()
