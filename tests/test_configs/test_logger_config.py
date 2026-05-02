import logging

import pytest

from src.configs.logger_config import setup_logger


class TestSetupLogger:
    @pytest.mark.unit
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger("test_setup_logger_a")
        assert isinstance(logger, logging.Logger)

    @pytest.mark.unit
    def test_logger_name_matches_argument(self) -> None:
        logger: logging.Logger = setup_logger("my_test_logger_b")
        assert logger.name == "my_test_logger_b"

    @pytest.mark.unit
    def test_logger_has_handlers(self) -> None:
        logger: logging.Logger = setup_logger("handler_test_logger_c")
        assert len(logger.handlers) > 0

    @pytest.mark.unit
    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("level_test_logger_d")
        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_calling_twice_does_not_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("dedup_logger_e")
        count: int = len(logger.handlers)
        setup_logger("dedup_logger_e")
        assert len(logger.handlers) == count

    @pytest.mark.unit
    def test_default_name_creates_valid_logger(self) -> None:
        logger: logging.Logger = setup_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == "python-flask-mongo-api-boilerplate"
