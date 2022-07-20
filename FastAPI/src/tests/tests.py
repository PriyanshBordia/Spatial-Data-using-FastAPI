from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)


def test_home() -> bool:
	try:
		response = client.get("/")
		assert response.status_code == 200
		assert response.json() == {"message": "API is fast.."}
		return True
	except Exception as e:
		return False

def test_country_id() -> bool:
	try:
		response = client.get("/country/id/1")
		assert response.status_code == 200
		assert response.json()["success"] == True
		response = client.get("/country/id/0")
		assert response.status_code == 200
		assert response.json()["success"] == False
		return True
	except Exception as e:
		return False

"""
{
  "admin": "Wakanda",
  "iso_a3": "WKA",
}
{
  "id": 257,
  "admin": "Atlantis",
  "iso_a3": "ATL",
  "geom": "00010001"
}
"""
