from typing import Any
from unittest.mock import patch

import pytest

from src.constants.defaults import DEFAULT_TEMPLATES
from src.models.template_model import TemplateModel
from src.startup.init_templates import add_default_templates


class TestAddDefaultTemplates:
    @pytest.mark.unit
    def test_does_nothing_when_templates_already_exist(self) -> None:
        existing: list[dict[str, Any]] = [{"_id": "1", "name": "hi"}]
        with (
            patch("src.startup.init_templates.TemplateService.get_all_templates", return_value=existing) as mock_get,
            patch("src.startup.init_templates.TemplateService.add_template") as mock_add,
        ):
            add_default_templates()
        mock_get.assert_called_once()
        mock_add.assert_not_called()

    @pytest.mark.unit
    def test_inserts_all_default_templates_when_collection_is_empty(self) -> None:
        with (
            patch("src.startup.init_templates.TemplateService.get_all_templates", return_value=[]),
            patch("src.startup.init_templates.TemplateService.add_template") as mock_add,
        ):
            add_default_templates()
        assert mock_add.call_count == len(DEFAULT_TEMPLATES)

    @pytest.mark.unit
    def test_inserts_correct_template_names(self) -> None:
        inserted: list[TemplateModel] = []
        with (
            patch("src.startup.init_templates.TemplateService.get_all_templates", return_value=[]),
            patch("src.startup.init_templates.TemplateService.add_template", side_effect=lambda m: inserted.append(m)),
        ):
            add_default_templates()
        inserted_names: list[str] = [m.name for m in inserted]
        expected_names: list[str] = [t["name"] for t in DEFAULT_TEMPLATES]
        assert inserted_names == expected_names

    @pytest.mark.unit
    def test_passes_template_model_instances_to_service(self) -> None:
        inserted: list[Any] = []
        with (
            patch("src.startup.init_templates.TemplateService.get_all_templates", return_value=[]),
            patch("src.startup.init_templates.TemplateService.add_template", side_effect=lambda m: inserted.append(m)),
        ):
            add_default_templates()
        for item in inserted:
            assert isinstance(item, TemplateModel)
