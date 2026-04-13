from .conftest import make_geom

# ─── Home / Response Structure ─────────────────────────────────────────────


def test_home(client):
	response = client.get("/")
	assert response.status_code == 200
	data = response.json()
	assert data["success"] is True
	assert data["meta"]["size"] == len(data["result"])
	assert data["message"] == "API is fast.."


def test_success_response_structure(client):
	data = client.get("/").json()
	assert "success" in data
	assert "meta" in data
	assert "size" in data["meta"]
	assert "result" in data
	assert "message" in data
	assert isinstance(data["result"], list)


def test_error_response_structure(client, seed_countries):
	data = client.get("/country/id/0").json()
	assert data["success"] is False
	assert "error" in data
	assert "message" in data["error"]
	assert isinstance(data["error"]["message"], list)


# ─── GET by ID ─────────────────────────────────────────────────────────────


def test_get_country_by_id(client, seed_countries):
	country = seed_countries[0]
	data = client.get(f"/country/id/{country.id}").json()
	assert data["success"] is True
	assert data["meta"]["size"] == 1
	assert data["result"][0]["id"] == country.id
	assert data["result"][0]["name"] == "Alphaland"
	assert data["result"][0]["code"] == "ALP"
	assert "coordinates" in data["result"][0]


def test_get_country_by_id_not_found(client, seed_countries):
	data = client.get("/country/id/0").json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0]


def test_get_country_by_id_negative(client, seed_countries):
	data = client.get("/country/id/-1").json()
	assert data["success"] is False


# ─── GET by Code ───────────────────────────────────────────────────────────


def test_get_country_by_code(client, seed_countries):
	data = client.get("/country/code/ALP").json()
	assert data["success"] is True
	assert data["result"][0]["code"] == "ALP"
	assert data["result"][0]["name"] == "Alphaland"


def test_get_country_by_code_case_insensitive(client, seed_countries):
	upper = client.get("/country/code/ALP").json()
	lower = client.get("/country/code/alp").json()
	mixed = client.get("/country/code/Alp").json()
	assert upper["success"] is True
	assert lower["success"] is True
	assert mixed["success"] is True
	assert upper["result"] == lower["result"] == mixed["result"]


def test_get_country_by_code_not_found(client, seed_countries):
	data = client.get("/country/code/ZZZ").json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0]


# ─── GET by Name ───────────────────────────────────────────────────────────


def test_get_country_by_name(client, seed_countries):
	data = client.get("/country/name/Alphaland").json()
	assert data["success"] is True
	assert data["result"][0]["name"] == "Alphaland"


def test_get_country_by_name_not_found(client, seed_countries):
	data = client.get("/country/name/Nonexistia").json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0]


# ─── GET by Name Contains ─────────────────────────────────────────────────


def test_get_country_name_contains(client, seed_countries):
	data = client.get("/country/name/contains/land").json()
	assert data["success"] is True
	assert data["meta"]["size"] >= 3
	names = [c["name"] for c in data["result"]]
	assert "Alphaland" in names
	assert "Betaland" in names
	assert "Gammaland" in names


def test_get_country_name_contains_partial(client, seed_countries):
	data = client.get("/country/name/contains/Alpha").json()
	assert data["success"] is True
	assert data["meta"]["size"] >= 1
	assert data["result"][0]["name"] == "Alphaland"


def test_get_country_name_contains_no_match(client, seed_countries):
	data = client.get("/country/name/contains/xyznonexistent").json()
	assert data["success"] is False


# ─── GET All Countries / Pagination ────────────────────────────────────────


def test_get_all_countries(client, seed_countries):
	data = client.get("/countries").json()
	assert data["success"] is True
	assert data["meta"]["size"] == len(data["result"])
	assert data["meta"]["size"] >= 3


def test_pagination_limit(client, seed_countries):
	data = client.get("/countries?skip=0&limit=2").json()
	assert data["success"] is True
	assert data["meta"]["size"] <= 2


def test_pagination_skip(client, seed_countries):
	all_data = client.get("/countries?skip=0&limit=1000").json()
	page1 = client.get("/countries?skip=0&limit=2").json()
	page2 = client.get("/countries?skip=2&limit=2").json()
	assert page1["success"] is True
	assert page2["success"] is True
	if all_data["meta"]["size"] > 2:
		page1_ids = {c["id"] for c in page1["result"]}
		page2_ids = {c["id"] for c in page2["result"]}
		assert page1_ids.isdisjoint(page2_ids)


def test_pagination_skip_beyond_total(client, seed_countries):
	data = client.get("/countries?skip=999999&limit=10").json()
	assert data["success"] is True
	assert data["meta"]["size"] == 0


# ─── Neighbors ─────────────────────────────────────────────────────────────


def test_get_neighbors_adjacent(client, seed_countries):
	alpha = seed_countries[0]
	data = client.get(f"/country/neighbors/{alpha.id}").json()
	assert data["success"] is True
	neighbor_codes = [c["code"] for c in data["result"]]
	assert "BET" in neighbor_codes


def test_get_neighbors_isolated(client, seed_countries):
	gamma = seed_countries[2]
	data = client.get(f"/country/neighbors/{gamma.id}").json()
	assert data["success"] is True
	# Isolated geometry should not neighbor the other seed countries
	neighbor_codes = [c["code"] for c in data["result"]]
	assert "ALP" not in neighbor_codes
	assert "BET" not in neighbor_codes


def test_get_neighbors_not_found(client, seed_countries):
	data = client.get("/country/neighbors/0").json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0]


# ─── Create ────────────────────────────────────────────────────────────────


def test_create_country(client, seed_countries, db):
	payload = {
		"admin": "Deltaland",
		"iso_a3": "DEL",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[5, 5], [5, 6], [6, 6], [6, 5], [5, 5]]]]},
	}
	data = client.post("/country/create/", json=payload).json()
	assert data["success"] is True
	assert data["result"][0]["name"] == "Deltaland"
	assert data["result"][0]["code"] == "DEL"
	assert "inserted" in data["message"].lower()
	# Cleanup
	from ..db.models import Country

	created_id = data["result"][0]["id"]
	db.query(Country).filter(Country.id == created_id).delete()
	db.commit()


def test_create_country_duplicate_name(client, seed_countries):
	payload = {
		"admin": "Alphaland",
		"iso_a3": "DUP",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[5, 5], [5, 6], [6, 6], [6, 5], [5, 5]]]]},
	}
	data = client.post("/country/create/", json=payload).json()
	assert data["success"] is False
	assert "already exists" in data["error"]["message"][0].lower()


def test_create_country_duplicate_code(client, seed_countries):
	payload = {
		"admin": "Unique",
		"iso_a3": "ALP",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[5, 5], [5, 6], [6, 6], [6, 5], [5, 5]]]]},
	}
	data = client.post("/country/create/", json=payload).json()
	assert data["success"] is False
	assert "already exists" in data["error"]["message"][0].lower()


def test_create_country_invalid_geom(client, seed_countries):
	payload = {"admin": "Badgeom", "iso_a3": "BAD", "geom": {"type": "Point", "coordinates": [0, 0]}}
	data = client.post("/country/create/", json=payload).json()
	assert data["success"] is False


def test_create_country_polygon_auto_converts(client, seed_countries, db):
	payload = {
		"admin": "Polyconvert",
		"iso_a3": "ZPC",
		"geom": {"type": "Polygon", "coordinates": [[[7, 7], [7, 8], [8, 8], [8, 7], [7, 7]]]},
	}
	data = client.post("/country/create/", json=payload).json()
	assert data["success"] is True
	assert data["result"][0]["name"] == "Polyconvert"
	# Cleanup
	from ..db.models import Country

	created_id = data["result"][0]["id"]
	db.query(Country).filter(Country.id == created_id).delete()
	db.commit()


# ─── Update ────────────────────────────────────────────────────────────────


def test_update_country(client, seed_countries):
	gamma = seed_countries[2]
	payload = {
		"admin": "Gammaland Updated",
		"iso_a3": "GAM",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[20, 20], [20, 21], [21, 21], [21, 20], [20, 20]]]]},
	}
	data = client.put(f"/country/update/{gamma.id}", json=payload).json()
	assert data["success"] is True
	assert data["result"][0]["name"] == "Gammaland Updated"
	assert "updated" in data["message"].lower()
	# Restore original name for other tests
	restore = {
		"admin": "Gammaland",
		"iso_a3": "GAM",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[20, 20], [20, 21], [21, 21], [21, 20], [20, 20]]]]},
	}
	client.put(f"/country/update/{gamma.id}", json=restore)


def test_update_country_not_found(client, seed_countries):
	payload = {
		"admin": "Ghost",
		"iso_a3": "GHO",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]]},
	}
	data = client.put("/country/update/0", json=payload).json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0].lower()


def test_update_country_duplicate_conflict(client, seed_countries):
	beta = seed_countries[1]
	payload = {
		"admin": "Alphaland",
		"iso_a3": "BET",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[1, 0], [1, 1], [2, 1], [2, 0], [1, 0]]]]},
	}
	data = client.put(f"/country/update/{beta.id}", json=payload).json()
	assert data["success"] is False
	assert "already exists" in data["error"]["message"][0].lower()


def test_update_country_invalid_geom(client, seed_countries):
	gamma = seed_countries[2]
	payload = {"admin": "Gammaland", "iso_a3": "GAM", "geom": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}}
	data = client.put(f"/country/update/{gamma.id}", json=payload).json()
	assert data["success"] is False


# ─── Delete ────────────────────────────────────────────────────────────────


def test_delete_country(client, db):
	from ..db.models import Country

	geom = make_geom([(30, 30), (30, 31), (31, 31), (31, 30), (30, 30)])
	disposable = Country(admin="Disposable", iso_a3="DSP", geom=geom)
	db.add(disposable)
	db.commit()
	db.refresh(disposable)

	data = client.delete(f"/country/delete/{disposable.id}").json()
	assert data["success"] is True
	assert data["result"][0]["name"] == "Disposable"
	assert "deleted" in data["message"].lower()

	verify = client.get(f"/country/id/{disposable.id}").json()
	assert verify["success"] is False


def test_delete_country_not_found(client, seed_countries):
	data = client.delete("/country/delete/0").json()
	assert data["success"] is False
	assert "does not exist" in data["error"]["message"][0].lower()


# ─── API Key Authentication ────────────────────────────────────────────────


def test_create_rejected_without_api_key(client, seed_countries, api_key):
	payload = {
		"admin": "Noauth",
		"iso_a3": "NAU",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]]},
	}
	response = client.post("/country/create/", json=payload)
	assert response.status_code == 403


def test_create_rejected_with_wrong_api_key(client, seed_countries, api_key):
	payload = {
		"admin": "Wrongkey",
		"iso_a3": "WRK",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]]},
	}
	response = client.post("/country/create/", json=payload, headers={"X-API-Key": "wrong-key"})
	assert response.status_code == 403


def test_create_accepted_with_correct_api_key(client, seed_countries, api_key, db):
	payload = {
		"admin": "Authed",
		"iso_a3": "ATH",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[9, 9], [9, 10], [10, 10], [10, 9], [9, 9]]]]},
	}
	response = client.post("/country/create/", json=payload, headers={"X-API-Key": api_key})
	assert response.status_code == 200
	data = response.json()
	assert data["success"] is True
	# Cleanup
	from ..db.models import Country

	db.query(Country).filter(Country.id == data["result"][0]["id"]).delete()
	db.commit()


def test_update_rejected_without_api_key(client, seed_countries, api_key):
	gamma = seed_countries[2]
	payload = {
		"admin": "Gammaland",
		"iso_a3": "GAM",
		"geom": {"type": "MultiPolygon", "coordinates": [[[[20, 20], [20, 21], [21, 21], [21, 20], [20, 20]]]]},
	}
	response = client.put(f"/country/update/{gamma.id}", json=payload)
	assert response.status_code == 403


def test_delete_rejected_without_api_key(client, seed_countries, api_key):
	alpha = seed_countries[0]
	response = client.delete(f"/country/delete/{alpha.id}")
	assert response.status_code == 403


# ─── Country Result Fields ─────────────────────────────────────────────────


def test_country_result_has_all_fields(client, seed_countries):
	country = seed_countries[0]
	data = client.get(f"/country/id/{country.id}").json()
	assert data["success"] is True
	result = data["result"][0]
	assert "id" in result
	assert "name" in result
	assert "code" in result
	assert "coordinates" in result
	assert isinstance(result["id"], int)
	assert isinstance(result["name"], str)
	assert isinstance(result["code"], str)
