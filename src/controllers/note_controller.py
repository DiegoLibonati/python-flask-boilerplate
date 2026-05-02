from flask import Response, jsonify, request

from src.constants.codes import CODE_SUCCESS_ADD_NOTE, CODE_SUCCESS_DELETE_NOTE, CODE_SUCCESS_GET_NOTES
from src.constants.messages import MESSAGE_SUCCESS_ADD_NOTE, MESSAGE_SUCCESS_DELETE_NOTE, MESSAGE_SUCCESS_GET_NOTES
from src.models.note_model import NoteModel
from src.services.note_service import NoteService
from src.utils.exceptions import InternalAPIError
from src.utils.exceptions_handler import exceptions_handler


@exceptions_handler
def alive() -> Response:
    response = {
        "message": "I am Alive!",
        "version_bp": "1.0.0",
        "author": "Diego Libonati",
        "name_bp": "Note",
    }

    return jsonify(response), 200


@exceptions_handler
def test_error() -> Response:
    raise InternalAPIError(code="CODE_NOTE_ERROR_TEST_MESSAGE", message="NoteError test message.")


@exceptions_handler
def create_note() -> Response:
    body = request.get_json() or {}
    note = NoteModel(**body)
    data = NoteService.add_note(note)

    return jsonify({"code": CODE_SUCCESS_ADD_NOTE, "message": MESSAGE_SUCCESS_ADD_NOTE, "data": data}), 201


@exceptions_handler
def get_notes() -> Response:
    data = NoteService.get_all_notes()

    return jsonify({"code": CODE_SUCCESS_GET_NOTES, "message": MESSAGE_SUCCESS_GET_NOTES, "data": data}), 200


@exceptions_handler
def delete_note(id: str) -> Response:
    NoteService.delete_note_by_id(id)

    return jsonify({"code": CODE_SUCCESS_DELETE_NOTE, "message": MESSAGE_SUCCESS_DELETE_NOTE}), 200
