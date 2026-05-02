from src.configs.default_config import DefaultConfig


class TestingConfig(DefaultConfig):
    TESTING = True
    DEBUG = True
    ENV = "testing"
