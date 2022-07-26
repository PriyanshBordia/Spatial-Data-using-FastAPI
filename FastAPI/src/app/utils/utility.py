import os

import geojson
from django.contrib.gis.geos import GEOSGeometry

from ..db import schemas


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
		response["error"]["message"].extend(error)
		return response
	except Exception as e:
		raise e

def populate_data():
	try:
		path = str(os.getcwd()) + "/src/app/data/countries.geojson"
		print(path)
		data = geojson.load(open(path, "r"))["features"]
		print(type(data))
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
			geom = (GEOSGeometry(geojson.dumps(geometry)).hexewkb).decode()
			country = schemas.CountryCreate(admin=admin, iso_a3=iso_a3, geom=geom)
			print(country.admin)
	except Exception as e:
		raise e