from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from bson import ObjectId
from pymongo.results import DeleteResult, InsertOneResult

from src.constants.codes import CODE_ALREADY_EXISTS_TEMPLATE, CODE_NOT_FOUND_TEMPLATE
from src.models.template_model import TemplateModel
from src.services.template_service import TemplateService
from src.utils.exceptions import ConflictAPIError, NotFoundAPIError


class TestAddTemplate:
    @pytest.mark.unit
    def test_adds_template_when_name_does_not_exist(self) -> None:
        model: TemplateModel = TemplateModel(name="new_template")
        mock_result: MagicMock = MagicMock(spec=InsertOneResult)
        with (
            patch("src.services.template_service.TemplateDAO.find_one_by_name", return_value=None) as mock_find,
            patch("src.services.template_service.TemplateDAO.insert_one", return_value=mock_result) as mock_insert,
        ):
            result = TemplateService.add_template(model)
        mock_find.assert_called_once_with("new_template")
        mock_insert.assert_called_once_with(model.model_dump())
        assert result == mock_result

    @pytest.mark.unit
    def test_raises_conflict_when_name_already_exists(self) -> None:
        model: TemplateModel = TemplateModel(name="existing")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "existing"}
        with patch("src.services.template_service.TemplateDAO.find_one_by_name", return_value=existing):
            with pytest.raises(ConflictAPIError) as exc_info:
                TemplateService.add_template(model)
        assert exc_info.value.code == CODE_ALREADY_EXISTS_TEMPLATE

    @pytest.mark.unit
    def test_conflict_error_has_409_status(self) -> None:
        model: TemplateModel = TemplateModel(name="existing")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "existing"}
        with patch("src.services.template_service.TemplateDAO.find_one_by_name", return_value=existing):
            with pytest.raises(ConflictAPIError) as exc_info:
                TemplateService.add_template(model)
        assert exc_info.value.status_code == 409

    @pytest.mark.unit
    def test_does_not_call_insert_when_conflict(self) -> None:
        model: TemplateModel = TemplateModel(name="dup")
        existing: dict[str, Any] = {"_id": str(ObjectId()), "name": "dup"}
        with (
            patch("src.services.template_service.TemplateDAO.find_one_by_name", return_value=existing),
            patch("src.services.template_service.TemplateDAO.insert_one") as mock_insert,
        ):
            with pytest.raises(ConflictAPIError):
                TemplateService.add_template(model)
        mock_insert.assert_not_called()


class TestGetAllTemplates:
    @pytest.mark.unit
    def test_returns_list_from_dao(self) -> None:
        expected: list[dict[str, Any]] = [{"_id": str(ObjectId()), "name": "tmpl"}]
        with patch("src.services.template_service.TemplateDAO.find", return_value=expected) as mock_find:
            result: list[dict[str, Any]] = TemplateService.get_all_templates()
        mock_find.assert_called_once()
        assert result == expected

    @pytest.mark.unit
    def test_returns_empty_list_when_no_templates(self) -> None:
        with patch("src.services.template_service.TemplateDAO.find", return_value=[]):
            result: list[dict[str, Any]] = TemplateService.get_all_templates()
        assert result == []

    @pytest.mark.unit
    def test_returns_multiple_templates(self) -> None:
        templates: list[dict[str, Any]] = [
            {"_id": str(ObjectId()), "name": "a"},
            {"_id": str(ObjectId()), "name": "b"},
        ]
        with patch("src.services.template_service.TemplateDAO.find", return_value=templates):
            result: list[dict[str, Any]] = TemplateService.get_all_templates()
        assert len(result) == 2


class TestDeleteTemplateById:
    @pytest.mark.unit
    def test_deletes_template_when_exists(self) -> None:
        _id: ObjectId = ObjectId()
        existing: dict[str, Any] = {"_id": str(_id), "name": "to_delete"}
        mock_result: MagicMock = MagicMock(spec=DeleteResult)
        with (
            patch("src.services.template_service.TemplateDAO.find_one_by_id", return_value=existing),
            patch("src.services.template_service.TemplateDAO.delete_one_by_id", return_value=mock_result) as mock_delete,
        ):
            result = TemplateService.delete_template_by_id(_id)
        mock_delete.assert_called_once_with(_id)
        assert result == mock_result

    @pytest.mark.unit
    def test_raises_not_found_when_template_does_not_exist(self) -> None:
        _id: ObjectId = ObjectId()
        with patch("src.services.template_service.TemplateDAO.find_one_by_id", return_value=None):
            with pytest.raises(NotFoundAPIError) as exc_info:
                TemplateService.delete_template_by_id(_id)
        assert exc_info.value.code == CODE_NOT_FOUND_TEMPLATE

    @pytest.mark.unit
    def test_not_found_error_has_404_status(self) -> None:
        _id: ObjectId = ObjectId()
        with patch("src.services.template_service.TemplateDAO.find_one_by_id", return_value=None):
            with pytest.raises(NotFoundAPIError) as exc_info:
                TemplateService.delete_template_by_id(_id)
        assert exc_info.value.status_code == 404

    @pytest.mark.unit
    def test_does_not_call_delete_when_not_found(self) -> None:
        _id: ObjectId = ObjectId()
        with (
            patch("src.services.template_service.TemplateDAO.find_one_by_id", return_value=None),
            patch("src.services.template_service.TemplateDAO.delete_one_by_id") as mock_delete,
        ):
            with pytest.raises(NotFoundAPIError):
                TemplateService.delete_template_by_id(_id)
        mock_delete.assert_not_called()
