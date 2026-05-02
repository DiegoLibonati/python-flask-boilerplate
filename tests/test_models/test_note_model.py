import pytest
from pydantic import ValidationError

from src.models.note_model import NoteModel


@pytest.mark.unit
class TestNoteModel:
    def test_creates_model_with_valid_name(self) -> None:
        note: NoteModel = NoteModel(name="hello")
        assert note.name == "hello"

    def test_strips_leading_and_trailing_whitespace(self) -> None:
        note: NoteModel = NoteModel(name="  hello  ")
        assert note.name == "hello"

    def test_strips_only_leading_whitespace(self) -> None:
        note: NoteModel = NoteModel(name="  hello")
        assert note.name == "hello"

    def test_raises_validation_error_for_empty_name(self) -> None:
        with pytest.raises(ValidationError):
            NoteModel(name="")

    def test_raises_validation_error_for_whitespace_only_name(self) -> None:
        with pytest.raises(ValidationError):
            NoteModel(name="   ")

    def test_raises_validation_error_when_name_is_missing(self) -> None:
        with pytest.raises(ValidationError):
            NoteModel()

    def test_model_dump_returns_dict_with_name(self) -> None:
        note: NoteModel = NoteModel(name="test")
        result: dict[str, str] = note.model_dump()
        assert result == {"name": "test"}

    def test_model_dump_returns_stripped_name(self) -> None:
        note: NoteModel = NoteModel(name="  test  ")
        result: dict[str, str] = note.model_dump()
        assert result == {"name": "test"}
