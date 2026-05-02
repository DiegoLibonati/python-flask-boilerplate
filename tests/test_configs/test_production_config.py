import pytest

from src.configs.production_config import ProductionConfig


class TestProductionConfig:
    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        assert ProductionConfig.DEBUG is False

    @pytest.mark.unit
    def test_env_is_production(self) -> None:
        assert ProductionConfig.ENV == "production"

    @pytest.mark.unit
    def test_inherits_json_as_ascii_false(self) -> None:
        assert ProductionConfig.JSON_AS_ASCII is False

    @pytest.mark.unit
    def test_inherits_testing_false(self) -> None:
        assert ProductionConfig.TESTING is False

    @pytest.mark.unit
    def test_inherits_mongo_uri(self) -> None:
        assert ProductionConfig.MONGO_URI.startswith("mongodb://")
