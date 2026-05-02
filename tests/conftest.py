import pytest

from app import create_app


@pytest.fixture(scope="session")
def app():
    flask_app = create_app("testing")
    yield flask_app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
