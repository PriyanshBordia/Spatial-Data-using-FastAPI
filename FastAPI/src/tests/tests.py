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
	assert response["error"]["code"] == ["Country with code: aux does not exist."]


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
	assert response["error"]["code"] == ["Country with name: Zulip does not exist."]


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


def test_create_country() -> bool:
	pass

def test_update_country() -> bool:
	pass

def test_delete_country() -> bool:
	pass

def test_get_neighbors() -> bool:
	response = client.get("/country/neighbors/1")
	assert response.status_code == 200
	response = response.json()
	assert response["success"] == True
	assert response["meta"]["size"] == len(response["result"])

	response = client.get("/country/neighbors/0")
	assert response.status_code == 200
	response = response.json()
	assert response["success"] == False



{
  "admin": "Aruba",
  "iso_a3": "ABW",
  "geom": {"type": "Polygon", "coordinates": [ [ [ -69.996937628999916, 12.577582098000036 ], [ -69.936390753999945, 12.531724351000051 ], [ -69.924672003999945, 12.519232489000046 ], [ -69.915760870999918, 12.497015692000076 ], [ -69.880197719999842, 12.453558661000045 ], [ -69.876820441999939, 12.427394924000097 ], [ -69.888091600999928, 12.417669989000046 ], [ -69.908802863999938, 12.417792059000107 ], [ -69.930531378999888, 12.425970770000035 ], [ -69.945139126999919, 12.44037506700009 ], [ -69.924672003999945, 12.44037506700009 ], [ -69.924672003999945, 12.447211005000014 ], [ -69.958566860999923, 12.463202216000099 ], [ -70.027658657999922, 12.522935289000088 ], [ -70.048085089999887, 12.531154690000079 ], [ -70.058094855999883, 12.537176825000088 ], [ -70.062408006999874, 12.546820380000057 ], [ -70.060373501999948, 12.556952216000113 ], [ -70.051096157999893, 12.574042059000064 ], [ -70.048736131999931, 12.583726304000024 ], [ -70.052642381999931, 12.600002346000053 ], [ -70.059641079999921, 12.614243882000054 ], [ -70.061105923999975, 12.625392971000068 ], [ -70.048736131999931, 12.632147528000104 ], [ -70.00715084499987, 12.5855166690001 ], [ -69.996937628999916, 12.577582098000036 ] ] ] }
}

