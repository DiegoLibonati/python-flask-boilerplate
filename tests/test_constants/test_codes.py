import pytest

from src.constants.codes import (
    CODE_ALREADY_EXISTS_NOTE,
    CODE_ERROR_AUTHENTICATION,
    CODE_ERROR_GENERIC,
    CODE_ERROR_INTERNAL_SERVER,
    CODE_ERROR_PYDANTIC,
    CODE_NOT_FOUND_NOTE,
    CODE_NOT_FOUND_ROUTE,
    CODE_NOT_VALID_INTEGER,
    CODE_SUCCESS_ADD_NOTE,
    CODE_SUCCESS_DELETE_NOTE,
    CODE_SUCCESS_GET_NOTES,
    CODE_SUCCESS_HEALTH,
    CODE_SUCCESS_READY,
)


@pytest.mark.unit
class TestCodes:
    def test_success_add_note_is_string(self) -> None:
        assert isinstance(CODE_SUCCESS_ADD_NOTE, str)

    def test_success_get_notes_is_string(self) -> None:
        assert isinstance(CODE_SUCCESS_GET_NOTES, str)

    def test_success_delete_note_is_string(self) -> None:
        assert isinstance(CODE_SUCCESS_DELETE_NOTE, str)

    def test_error_internal_server_is_string(self) -> None:
        assert isinstance(CODE_ERROR_INTERNAL_SERVER, str)

    def test_error_pydantic_is_string(self) -> None:
        assert isinstance(CODE_ERROR_PYDANTIC, str)

    def test_error_authentication_is_string(self) -> None:
        assert isinstance(CODE_ERROR_AUTHENTICATION, str)

    def test_error_generic_is_string(self) -> None:
        assert isinstance(CODE_ERROR_GENERIC, str)

    def test_not_valid_integer_is_string(self) -> None:
        assert isinstance(CODE_NOT_VALID_INTEGER, str)

    def test_already_exists_note_is_string(self) -> None:
        assert isinstance(CODE_ALREADY_EXISTS_NOTE, str)

    def test_not_found_note_is_string(self) -> None:
        assert isinstance(CODE_NOT_FOUND_NOTE, str)

    def test_not_found_route_is_string(self) -> None:
        assert isinstance(CODE_NOT_FOUND_ROUTE, str)

    def test_success_health_is_string(self) -> None:
        assert isinstance(CODE_SUCCESS_HEALTH, str)

    def test_success_ready_is_string(self) -> None:
        assert isinstance(CODE_SUCCESS_READY, str)

    def test_all_codes_are_unique(self) -> None:
        codes: list[str] = [
            CODE_SUCCESS_ADD_NOTE,
            CODE_SUCCESS_GET_NOTES,
            CODE_SUCCESS_DELETE_NOTE,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_GENERIC,
            CODE_ERROR_AUTHENTICATION,
            CODE_NOT_VALID_INTEGER,
            CODE_ALREADY_EXISTS_NOTE,
            CODE_NOT_FOUND_NOTE,
        ]
        assert len(codes) == len(set(codes))

    def test_all_codes_are_non_empty(self) -> None:
        codes: list[str] = [
            CODE_SUCCESS_ADD_NOTE,
            CODE_SUCCESS_GET_NOTES,
            CODE_SUCCESS_DELETE_NOTE,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_GENERIC,
            CODE_ERROR_AUTHENTICATION,
            CODE_NOT_VALID_INTEGER,
            CODE_ALREADY_EXISTS_NOTE,
            CODE_NOT_FOUND_NOTE,
        ]
        for code in codes:
            assert code != ""
