import uuid
from datetime import UTC, datetime
from typing import Any

_store: list[dict[str, Any]] = []


class NoteDAO:
    @staticmethod
    def insert_one(note: dict[str, Any]) -> dict[str, Any]:
        entry = {
            "_id": str(uuid.uuid4()),
            "created_at": datetime.now(UTC).isoformat(),
            **note,
        }
        _store.append(entry)
        return entry

    @staticmethod
    def find() -> list[dict[str, Any]]:
        return list(_store)

    @staticmethod
    def find_one_by_id(_id: str) -> dict[str, Any] | None:
        return next((n for n in _store if n["_id"] == _id), None)

    @staticmethod
    def find_one_by_name(name: str) -> dict[str, Any] | None:
        return next((n for n in _store if n["name"].lower() == name.lower()), None)

    @staticmethod
    def delete_one_by_id(_id: str) -> bool:
        global _store
        original_len = len(_store)
        _store = [n for n in _store if n["_id"] != _id]
        return len(_store) < original_len
