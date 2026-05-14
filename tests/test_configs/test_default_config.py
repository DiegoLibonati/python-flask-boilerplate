import pytest

from src.configs.default_config import DefaultConfig


@pytest.mark.unit
class TestDefaultConfig:
    def test_debug_is_false(self) -> None:
        assert DefaultConfig.DEBUG is False

    def test_testing_is_false(self) -> None:
        assert DefaultConfig.TESTING is False

    def test_has_tz_attribute(self) -> None:
        assert hasattr(DefaultConfig, "TZ")

    def test_has_host_attribute(self) -> None:
        assert hasattr(DefaultConfig, "HOST")

    def test_has_port_attribute(self) -> None:
        assert hasattr(DefaultConfig, "PORT")

    def test_tz_is_string(self) -> None:
        assert isinstance(DefaultConfig.TZ, str)

    def test_tz_is_non_empty(self) -> None:
        assert DefaultConfig.TZ != ""
