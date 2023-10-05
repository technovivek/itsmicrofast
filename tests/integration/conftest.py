import pytest

from tests.integration.fixtures.database import * # noqa F403
from tests.integration.fixtures.operations import * # noqa F403
from fastapi.testclient import TestClient
from fastapi import FastAPI
from api import app
from tests.integration.fixtures.database import * # noqa F403

# client = FastAPI()

client = TestClient(app)

@pytest.fixture
def test_app_client(scope="module"):
    return client





