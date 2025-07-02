import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Test client for the FastAPI application
    """
    return TestClient(app)
