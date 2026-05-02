import pytest

from src.configs.default_config import DefaultConfig
from src.configs.production_config import ProductionConfig


@pytest.mark.unit
class TestProductionConfig:
    def test_debug_is_false(self) -> None:
        assert ProductionConfig.DEBUG is False

    def test_env_is_production(self) -> None:
        assert ProductionConfig.ENV == "production"

    def test_inherits_from_default_config(self) -> None:
        assert issubclass(ProductionConfig, DefaultConfig)

    def test_json_as_ascii_inherited_as_false(self) -> None:
        assert ProductionConfig.JSON_AS_ASCII is False
