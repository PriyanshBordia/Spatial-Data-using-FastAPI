import geojson
from ..db import schemas
from django.contrib.gis.geos import GEOSGeometry


def format(country) -> dict:
	try:
		id = country.id
		admin = country.admin
		code = country.iso_a3
		geom = GEOSGeometry(str(country.geom)).geojson
		coordinates = geojson.loads(geom).get("coordinates")
		return {"id": id, "name": admin, "code": code, "coordinates": coordinates}
	except Exception as e:
		raise e


def success_response(data: list, message="API is fast..") -> dict:
	try:
		response = {"message": "", "meta": {"size": 0}, "result": [], "success": True}
		response["message"] = message
		response["meta"]["size"] = len(data)
		response["result"].extend(data)
		return response
	except Exception as e:
		raise e


def error_response(error: list) -> dict:
	try:	
		response = {"error": {"message": []}, "success": False}
		response["error"]["code"].extend(error)
		return response
	except Exception as e:
		raise e

def populate_data():
	try:
		data = geojson.load(open("countries.geojson"))["features"]
		for row in data:
			properties = row["properties"]
			geometry = row["geometry"]
			admin = properties.get("ADMIN")
			iso_a3 = properties.get("ISO_A3")
			if geometry.get("type") == "Polygon":
				points = [geometry.get("coordinates")]
			elif geometry.get("type") == "MultiPolygon":
				points = geometry.get("coordinates")
			else:
				print(f"Error: {admin} ")
			geom = geojson.MultiPolygon(points)
			country = schemas.CountryCreate(admin=admin, iso_a3=iso_a3, geom=geom)
	except Exception as e:
		raise e