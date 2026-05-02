import pytest

from src.constants.defaults import DEFAULT_NOTES, DEFAULT_VALUE


@pytest.mark.unit
class TestDefaults:
    def test_default_value_is_zero(self) -> None:
        assert DEFAULT_VALUE == 0

    def test_default_value_is_integer(self) -> None:
        assert isinstance(DEFAULT_VALUE, int)

    def test_default_notes_is_list(self) -> None:
        assert isinstance(DEFAULT_NOTES, list)

    def test_default_notes_has_two_entries(self) -> None:
        assert len(DEFAULT_NOTES) == 2

    def test_each_default_note_has_name_key(self) -> None:
        for note in DEFAULT_NOTES:
            assert "name" in note

    def test_each_default_note_name_is_non_empty_string(self) -> None:
        for note in DEFAULT_NOTES:
            assert isinstance(note["name"], str)
            assert note["name"] != ""

    def test_default_note_names_are_unique(self) -> None:
        names: list[str] = [note["name"] for note in DEFAULT_NOTES]
        assert len(names) == len(set(names))
