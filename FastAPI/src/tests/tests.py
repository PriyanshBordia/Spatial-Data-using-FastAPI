from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)


def test_home() -> bool:
    response = client.get("/")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])
    assert response["message"] == "API is fast.."


def test_country_id() -> bool:
    response = client.get("/country/id/1")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])
    assert response["result"][0]["id"] == 1

    response = client.get("/country/id/0")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == False
    assert response["error"]["code"] == ["Country with id: 0 does not exist."]


def test_country_code() -> bool:
    response = client.get("/country/code/ind")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])
    assert response["result"][0]["code"] == "IND"

    response = client.get("/country/code/aux")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == False
    assert response["error"]["code"] == [
        "Country with code: aux does not exist."]


def test_country_name() -> bool:
    response = client.get("/country/name/India")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])
    assert response["result"][0]["name"] == "India"

    response = client.get("/country/name/Zulip")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == False
    assert response["error"]["code"] == [
        "Country with name: Zulip does not exist."]


def test_country_name_contains() -> bool:
    response = client.get("/country/name/contains/ia")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])


def test_countries() -> bool:
    response = client.get("/countries")
    assert response.status_code == 200
    response = response.json()
    assert response["success"] == True
    assert response["meta"]["size"] == len(response["result"])
