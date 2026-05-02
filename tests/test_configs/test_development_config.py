import pytest

from src.configs.development_config import DevelopmentConfig


class TestDevelopmentConfig:
    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        assert DevelopmentConfig.DEBUG is True

    @pytest.mark.unit
    def test_env_is_development(self) -> None:
        assert DevelopmentConfig.ENV == "development"

    @pytest.mark.unit
    def test_inherits_json_as_ascii_false(self) -> None:
        assert DevelopmentConfig.JSON_AS_ASCII is False

    @pytest.mark.unit
    def test_inherits_testing_false(self) -> None:
        assert DevelopmentConfig.TESTING is False

    @pytest.mark.unit
    def test_inherits_mongo_uri(self) -> None:
        assert DevelopmentConfig.MONGO_URI.startswith("mongodb://")
