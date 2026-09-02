import logging

import pytest

from src.configs.logger_config import setup_logger


@pytest.mark.unit
class TestSetupLogger:
    def test_returns_logger_instance(self) -> None:
        logger: logging.Logger = setup_logger()
        assert isinstance(logger, logging.Logger)

    def test_default_name_is_project_name(self) -> None:
        logger: logging.Logger = setup_logger()
        assert logger.name == "python-flask-boilerplate"

    def test_custom_name_is_applied(self) -> None:
        logger: logging.Logger = setup_logger("my-custom-logger")
        assert logger.name == "my-custom-logger"

    def test_logger_has_at_least_one_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-handler-logger")
        assert len(logger.handlers) > 0

    def test_logger_level_is_debug(self) -> None:
        logger: logging.Logger = setup_logger("test-level-logger")
        assert logger.level == logging.DEBUG

    def test_calling_twice_does_not_duplicate_handlers(self) -> None:
        logger: logging.Logger = setup_logger("test-no-dup-logger")
        count_first: int = len(logger.handlers)
        setup_logger("test-no-dup-logger")
        assert len(logger.handlers) == count_first

    def test_handler_is_stream_handler(self) -> None:
        logger: logging.Logger = setup_logger("test-stream-handler-logger")
        assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)
