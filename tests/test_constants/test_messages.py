import pytest

from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_NOTE,
    MESSAGE_ERROR_AUTHENTICATION,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_INTERNAL_SERVER,
    MESSAGE_ERROR_PYDANTIC,
    MESSAGE_NOT_FOUND_NOTE,
    MESSAGE_NOT_FOUND_ROUTE,
    MESSAGE_NOT_VALID_INTEGER,
    MESSAGE_SUCCESS_ADD_NOTE,
    MESSAGE_SUCCESS_DELETE_NOTE,
    MESSAGE_SUCCESS_GET_NOTES,
    MESSAGE_SUCCESS_HEALTH,
    MESSAGE_SUCCESS_READY,
)


@pytest.mark.unit
class TestMessages:
    def test_success_add_note_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_ADD_NOTE, str)

    def test_success_get_notes_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_GET_NOTES, str)

    def test_success_delete_note_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_DELETE_NOTE, str)

    def test_error_internal_server_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_INTERNAL_SERVER, str)

    def test_error_pydantic_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_PYDANTIC, str)

    def test_error_authentication_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_AUTHENTICATION, str)

    def test_error_generic_is_string(self) -> None:
        assert isinstance(MESSAGE_ERROR_GENERIC, str)

    def test_not_valid_integer_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_VALID_INTEGER, str)

    def test_already_exists_note_is_string(self) -> None:
        assert isinstance(MESSAGE_ALREADY_EXISTS_NOTE, str)

    def test_not_found_note_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_NOTE, str)

    def test_not_found_route_is_string(self) -> None:
        assert isinstance(MESSAGE_NOT_FOUND_ROUTE, str)

    def test_success_health_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_HEALTH, str)

    def test_success_ready_is_string(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_READY, str)

    def test_all_messages_are_non_empty(self) -> None:
        messages: list[str] = [
            MESSAGE_SUCCESS_ADD_NOTE,
            MESSAGE_SUCCESS_GET_NOTES,
            MESSAGE_SUCCESS_DELETE_NOTE,
            MESSAGE_ERROR_INTERNAL_SERVER,
            MESSAGE_ERROR_PYDANTIC,
            MESSAGE_ERROR_GENERIC,
            MESSAGE_ERROR_AUTHENTICATION,
            MESSAGE_NOT_VALID_INTEGER,
            MESSAGE_ALREADY_EXISTS_NOTE,
            MESSAGE_NOT_FOUND_NOTE,
        ]
        for message in messages:
            assert message != ""
