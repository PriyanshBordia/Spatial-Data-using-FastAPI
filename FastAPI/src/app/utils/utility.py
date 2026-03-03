import os

import geojson
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
from shapely.geometry import mapping, shape

from ..db import models


def format_country(country) -> dict:
	geom = to_shape(country.geom)
	coordinates = mapping(geom).get("coordinates")
	return {"id": country.id, "name": country.admin, "code": country.iso_a3, "coordinates": coordinates}


def normalize_geometry(geometry_dict):
	"""Convert a GeoJSON geometry dict to a WKBElement for DB storage.
	Converts Polygon to MultiPolygon. Returns None for unsupported types."""
	geom_type = geometry_dict.get("type")
	if geom_type == "Polygon":
		geometry_dict = {
			"type": "MultiPolygon",
			"coordinates": [geometry_dict.get("coordinates")]
		}
	elif geom_type != "MultiPolygon":
		return None
	geom_shape = shape(geometry_dict)
	return from_shape(geom_shape, srid=4326)


def success_response(data: list, message="API is fast..") -> dict:
	response = {"message": "", "meta": {"size": 0}, "result": [], "success": True}
	response["message"] = message
	response["meta"]["size"] = len(data)
	response["result"].extend(data)
	return response


def error_response(error: list) -> dict:
	response = {"error": {"message": []}, "success": False}
	response["error"]["message"].extend(error)
	return response


def populate_data(db):
	path = str(os.getcwd()) + "/src/app/data/countries.geojson"
	with open(path, "r") as f:
		data = geojson.load(f)["features"]
	for row in data:
		properties = row["properties"]
		geometry = row["geometry"]
		admin = properties.get("ADMIN")
		iso_a3 = properties.get("ISO_A3")
		geom_shape = shape(geometry)
		if geom_shape.geom_type == "Polygon":
			geom_shape = ShapelyMultiPolygon([geom_shape])
		wkb_element = from_shape(geom_shape, srid=4326)
		db.add(models.Country(admin=admin, iso_a3=iso_a3, geom=wkb_element))
	db.commit()
