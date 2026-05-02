from src.constants.defaults import DEFAULT_TEMPLATES
from src.models.template_model import TemplateModel
from src.services.template_service import TemplateService


def add_default_templates() -> None:
    templates = TemplateService.get_all_templates()

    if templates:
        return

    for default_template in DEFAULT_TEMPLATES:
        TemplateService.add_template(TemplateModel(**default_template))
