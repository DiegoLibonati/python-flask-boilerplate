import pytest

from src.configs.default_config import DefaultConfig


class TestDefaultConfig:
    @pytest.mark.unit
    def test_debug_is_false(self) -> None:
        assert DefaultConfig.DEBUG is False

    @pytest.mark.unit
    def test_testing_is_false(self) -> None:
        assert DefaultConfig.TESTING is False

    @pytest.mark.unit
    def test_json_as_ascii_is_false(self) -> None:
        assert DefaultConfig.JSON_AS_ASCII is False

    @pytest.mark.unit
    def test_mongo_uri_starts_with_mongodb(self) -> None:
        assert DefaultConfig.MONGO_URI.startswith("mongodb://")

    @pytest.mark.unit
    def test_mongo_uri_contains_auth_source(self) -> None:
        assert "authSource" in DefaultConfig.MONGO_URI

    @pytest.mark.unit
    def test_mongo_db_name_is_non_empty_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_DB_NAME, str)
        assert len(DefaultConfig.MONGO_DB_NAME) > 0

    @pytest.mark.unit
    def test_mongo_host_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_HOST, str)

    @pytest.mark.unit
    def test_mongo_user_is_string(self) -> None:
        assert isinstance(DefaultConfig.MONGO_USER, str)
