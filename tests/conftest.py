import os
import subprocess
import time
from collections.abc import Generator

import pymongo
import pytest
from flask import Flask
from flask.testing import FlaskClient
from pymongo.database import Database

from app import create_app


def start_test_database() -> None:
    subprocess.run(
        ["docker", "compose", "-f", "test.docker-compose.yml", "up", "-d"],
        check=True,
    )


def stop_test_database() -> None:
    subprocess.run(
        ["docker", "compose", "-f", "test.docker-compose.yml", "down", "-v"],
        check=True,
    )


def wait_for_mongo(host: str, port: int, timeout: int = 30) -> None:
    deadline: float = time.time() + timeout
    while time.time() < deadline:
        try:
            client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=1000)
            client.admin.command("ping")
            client.close()
            return
        except Exception:
            time.sleep(1)
    raise TimeoutError(f"MongoDB did not become ready on {host}:{port} within {timeout}s")


@pytest.fixture(scope="session")
@pytest.mark.timeout(60)
def database_container() -> Generator[None, None, None]:
    start_test_database()
    host: str = os.environ.get("TEST_MONGO_HOST", "localhost")
    port: int = int(os.environ.get("TEST_MONGO_PORT", "27017"))
    wait_for_mongo(host, port)
    yield
    stop_test_database()


@pytest.fixture(scope="session")
def app(database_container: None) -> Generator[Flask, None, None]:
    flask_app = create_app("testing")
    yield flask_app


@pytest.fixture(scope="function")
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture(scope="function")
def mongo_db(database_container: None) -> Generator[Database, None, None]:
    uri: str = os.environ.get("MONGO_URI", "")
    db_name: str = os.environ.get("MONGO_DB_NAME", "test_db")
    mongo_client = pymongo.MongoClient(uri)
    db = mongo_client[db_name]
    yield db
    db.client.drop_database(db_name)
    mongo_client.close()
