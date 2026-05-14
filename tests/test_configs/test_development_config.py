import pytest

from src.configs.default_config import DefaultConfig
from src.configs.development_config import DevelopmentConfig


@pytest.mark.unit
class TestDevelopmentConfig:
    def test_debug_is_true(self) -> None:
        assert DevelopmentConfig.DEBUG is True

    def test_env_is_development(self) -> None:
        assert DevelopmentConfig.ENV == "development"

    def test_inherits_from_default_config(self) -> None:
        assert issubclass(DevelopmentConfig, DefaultConfig)
