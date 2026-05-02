import pytest

from src.configs.testing_config import TestingConfig


class TestTestingConfig:
    @pytest.mark.unit
    def test_testing_is_true(self) -> None:
        assert TestingConfig.TESTING is True

    @pytest.mark.unit
    def test_debug_is_true(self) -> None:
        assert TestingConfig.DEBUG is True

    @pytest.mark.unit
    def test_env_is_testing(self) -> None:
        assert TestingConfig.ENV == "testing"

    @pytest.mark.unit
    def test_mongo_uri_is_non_empty_string(self) -> None:
        assert isinstance(TestingConfig.MONGO_URI, str)
        assert len(TestingConfig.MONGO_URI) > 0

    @pytest.mark.unit
    def test_mongo_db_name_is_non_empty_string(self) -> None:
        assert isinstance(TestingConfig.MONGO_DB_NAME, str)
        assert len(TestingConfig.MONGO_DB_NAME) > 0

    @pytest.mark.unit
    def test_mongo_uri_starts_with_mongodb(self) -> None:
        assert TestingConfig.MONGO_URI.startswith("mongodb://")
