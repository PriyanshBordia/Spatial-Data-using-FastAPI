from unittest import TestResult

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is fast.."}
