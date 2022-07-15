from unittest import TestResult

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is fast.."}

"""
{
  "id": 256,
  "admin": "Wakanda",
  "iso_a3": "WKA",
  "geom": "0000"
}
{
  "id": 257,
  "admin": "Atlantis",
  "iso_a3": "ATL",
  "geom": "00010001"
}
"""