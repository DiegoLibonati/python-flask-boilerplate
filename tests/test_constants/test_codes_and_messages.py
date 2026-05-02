import pytest

from src.constants.codes import (
    CODE_ALREADY_EXISTS_TEMPLATE,
    CODE_ERROR_AUTHENTICATION,
    CODE_ERROR_DATABASE,
    CODE_ERROR_GENERIC,
    CODE_ERROR_INTERNAL_SERVER,
    CODE_ERROR_PYDANTIC,
    CODE_NOT_FOUND_TEMPLATE,
    CODE_NOT_VALID_INTEGER,
    CODE_SUCCESS_ADD_TEMPLATE,
)
from src.constants.messages import (
    MESSAGE_ALREADY_EXISTS_TEMPLATE,
    MESSAGE_ERROR_AUTHENTICATION,
    MESSAGE_ERROR_DATABASE,
    MESSAGE_ERROR_GENERIC,
    MESSAGE_ERROR_INTERNAL_SERVER,
    MESSAGE_ERROR_PYDANTIC,
    MESSAGE_NOT_FOUND_TEMPLATE,
    MESSAGE_NOT_VALID_INTEGER,
    MESSAGE_SUCCESS_ADD_TEMPLATE,
)


class TestCodes:
    @pytest.mark.unit
    def test_code_success_add_template(self) -> None:
        assert CODE_SUCCESS_ADD_TEMPLATE == "SUCCESS_ADD_TEMPLATE"

    @pytest.mark.unit
    def test_code_error_internal_server(self) -> None:
        assert CODE_ERROR_INTERNAL_SERVER == "ERROR_INTERNAL_SERVER"

    @pytest.mark.unit
    def test_code_error_pydantic(self) -> None:
        assert CODE_ERROR_PYDANTIC == "ERROR_PYDANTIC"

    @pytest.mark.unit
    def test_code_error_database(self) -> None:
        assert CODE_ERROR_DATABASE == "ERROR_DATABASE"

    @pytest.mark.unit
    def test_code_already_exists_template(self) -> None:
        assert CODE_ALREADY_EXISTS_TEMPLATE == "ALREADY_EXISTS_TEMPLATE"

    @pytest.mark.unit
    def test_code_not_found_template(self) -> None:
        assert CODE_NOT_FOUND_TEMPLATE == "NOT_FOUND_TEMPLATE"

    @pytest.mark.unit
    def test_all_codes_are_non_empty_strings(self) -> None:
        codes: list[str] = [
            CODE_SUCCESS_ADD_TEMPLATE,
            CODE_ERROR_INTERNAL_SERVER,
            CODE_ERROR_PYDANTIC,
            CODE_ERROR_DATABASE,
            CODE_ERROR_GENERIC,
            CODE_ERROR_AUTHENTICATION,
            CODE_NOT_VALID_INTEGER,
            CODE_ALREADY_EXISTS_TEMPLATE,
            CODE_NOT_FOUND_TEMPLATE,
        ]
        for code in codes:
            assert isinstance(code, str)
            assert len(code) > 0


class TestMessages:
    @pytest.mark.unit
    def test_message_success_add_template_is_non_empty(self) -> None:
        assert isinstance(MESSAGE_SUCCESS_ADD_TEMPLATE, str)
        assert len(MESSAGE_SUCCESS_ADD_TEMPLATE) > 0

    @pytest.mark.unit
    def test_message_error_internal_server_is_non_empty(self) -> None:
        assert isinstance(MESSAGE_ERROR_INTERNAL_SERVER, str)
        assert len(MESSAGE_ERROR_INTERNAL_SERVER) > 0

    @pytest.mark.unit
    def test_message_already_exists_template(self) -> None:
        assert MESSAGE_ALREADY_EXISTS_TEMPLATE == "Template already exists."

    @pytest.mark.unit
    def test_message_not_found_template(self) -> None:
        assert MESSAGE_NOT_FOUND_TEMPLATE == "No template found."

    @pytest.mark.unit
    def test_all_messages_are_non_empty_strings(self) -> None:
        messages: list[str] = [
            MESSAGE_SUCCESS_ADD_TEMPLATE,
            MESSAGE_ERROR_INTERNAL_SERVER,
            MESSAGE_ERROR_PYDANTIC,
            MESSAGE_ERROR_DATABASE,
            MESSAGE_ERROR_GENERIC,
            MESSAGE_ERROR_AUTHENTICATION,
            MESSAGE_NOT_VALID_INTEGER,
            MESSAGE_ALREADY_EXISTS_TEMPLATE,
            MESSAGE_NOT_FOUND_TEMPLATE,
        ]
        for message in messages:
            assert isinstance(message, str)
            assert len(message) > 0
