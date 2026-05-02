import pytest

import src.configs.gunicorn_config as gunicorn_config


@pytest.mark.unit
class TestGunicornConfig:
    def test_bind_address(self) -> None:
        assert gunicorn_config.bind == "0.0.0.0:5050"

    def test_workers_is_positive_integer(self) -> None:
        assert isinstance(gunicorn_config.workers, int)
        assert gunicorn_config.workers > 0

    def test_threads_is_two(self) -> None:
        assert gunicorn_config.threads == 2

    def test_timeout_is_120(self) -> None:
        assert gunicorn_config.timeout == 120

    def test_graceful_timeout_is_30(self) -> None:
        assert gunicorn_config.graceful_timeout == 30

    def test_accesslog_is_stdout(self) -> None:
        assert gunicorn_config.accesslog == "-"

    def test_errorlog_is_stdout(self) -> None:
        assert gunicorn_config.errorlog == "-"

    def test_loglevel_is_info(self) -> None:
        assert gunicorn_config.loglevel == "info"

    def test_proc_name(self) -> None:
        assert gunicorn_config.proc_name == "boilerplate-server"
