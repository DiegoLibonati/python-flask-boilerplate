from typing import Any

import pytest

from src.data_access import note_dao
from src.data_access.note_dao import NoteDAO


@pytest.fixture(autouse=True)
def reset_store() -> None:
    note_dao._store.clear()


@pytest.mark.unit
class TestNoteDAOInsertOne:
    def test_returns_entry_with_generated_id(self) -> None:
        result: dict[str, Any] = NoteDAO.insert_one({"name": "test"})
        assert "_id" in result

    def test_returns_entry_with_created_at(self) -> None:
        result: dict[str, Any] = NoteDAO.insert_one({"name": "test"})
        assert "created_at" in result

    def test_returns_entry_with_original_fields(self) -> None:
        result: dict[str, Any] = NoteDAO.insert_one({"name": "test"})
        assert result["name"] == "test"

    def test_inserted_entry_is_present_in_store(self) -> None:
        NoteDAO.insert_one({"name": "test"})
        assert len(NoteDAO.find()) == 1

    def test_assigns_unique_ids_to_consecutive_inserts(self) -> None:
        first: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        second: dict[str, Any] = NoteDAO.insert_one({"name": "b"})
        assert first["_id"] != second["_id"]

    def test_multiple_inserts_accumulate_in_store(self) -> None:
        NoteDAO.insert_one({"name": "a"})
        NoteDAO.insert_one({"name": "b"})
        NoteDAO.insert_one({"name": "c"})
        assert len(NoteDAO.find()) == 3


@pytest.mark.unit
class TestNoteDAOFind:
    def test_returns_empty_list_when_store_is_empty(self) -> None:
        result: list[dict[str, Any]] = NoteDAO.find()
        assert result == []

    def test_returns_all_inserted_entries(self) -> None:
        NoteDAO.insert_one({"name": "a"})
        NoteDAO.insert_one({"name": "b"})
        result: list[dict[str, Any]] = NoteDAO.find()
        assert len(result) == 2

    def test_returns_a_copy_not_the_internal_list(self) -> None:
        NoteDAO.insert_one({"name": "a"})
        result: list[dict[str, Any]] = NoteDAO.find()
        result.clear()
        assert len(NoteDAO.find()) == 1


@pytest.mark.unit
class TestNoteDAOFindOneById:
    def test_returns_entry_when_id_exists(self) -> None:
        inserted: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        result: dict[str, Any] | None = NoteDAO.find_one_by_id(inserted["_id"])
        assert result is not None
        assert result["_id"] == inserted["_id"]

    def test_returns_none_when_id_does_not_exist(self) -> None:
        result: dict[str, Any] | None = NoteDAO.find_one_by_id("nonexistent")
        assert result is None

    def test_returns_correct_entry_when_multiple_exist(self) -> None:
        NoteDAO.insert_one({"name": "a"})
        target: dict[str, Any] = NoteDAO.insert_one({"name": "b"})
        NoteDAO.insert_one({"name": "c"})
        result: dict[str, Any] | None = NoteDAO.find_one_by_id(target["_id"])
        assert result is not None
        assert result["name"] == "b"


@pytest.mark.unit
class TestNoteDAOFindOneByName:
    def test_returns_entry_when_name_matches(self) -> None:
        NoteDAO.insert_one({"name": "hello"})
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("hello")
        assert result is not None
        assert result["name"] == "hello"

    def test_search_is_case_insensitive(self) -> None:
        NoteDAO.insert_one({"name": "Hello"})
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("hello")
        assert result is not None

    def test_search_is_case_insensitive_uppercase(self) -> None:
        NoteDAO.insert_one({"name": "hello"})
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("HELLO")
        assert result is not None

    def test_returns_none_when_name_does_not_exist(self) -> None:
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("missing")
        assert result is None

    def test_returns_none_when_store_is_empty(self) -> None:
        result: dict[str, Any] | None = NoteDAO.find_one_by_name("anything")
        assert result is None


@pytest.mark.unit
class TestNoteDAODeleteOneById:
    def test_returns_true_when_entry_is_deleted(self) -> None:
        inserted: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        result: bool = NoteDAO.delete_one_by_id(inserted["_id"])
        assert result is True

    def test_returns_false_when_id_does_not_exist(self) -> None:
        result: bool = NoteDAO.delete_one_by_id("nonexistent")
        assert result is False

    def test_removes_entry_from_store(self) -> None:
        inserted: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        NoteDAO.delete_one_by_id(inserted["_id"])
        assert NoteDAO.find_one_by_id(inserted["_id"]) is None

    def test_store_is_empty_after_deleting_only_entry(self) -> None:
        inserted: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        NoteDAO.delete_one_by_id(inserted["_id"])
        assert NoteDAO.find() == []

    def test_does_not_remove_other_entries(self) -> None:
        first: dict[str, Any] = NoteDAO.insert_one({"name": "a"})
        second: dict[str, Any] = NoteDAO.insert_one({"name": "b"})
        NoteDAO.delete_one_by_id(first["_id"])
        remaining: list[dict[str, Any]] = NoteDAO.find()
        assert len(remaining) == 1
        assert remaining[0]["_id"] == second["_id"]
