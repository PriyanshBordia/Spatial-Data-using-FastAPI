from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import mapping, shape

from .exceptions import InvalidGeometryError


def to_wkb_multipolygon(geometry_dict: dict):
	"""Convert a GeoJSON geometry dict to a WKBElement for DB storage.

	Polygon is auto-promoted to MultiPolygon. Raises InvalidGeometryError
	for unsupported geometry types.
	"""
	geom_type = geometry_dict.get("type")
	if geom_type == "Polygon":
		geometry_dict = {
			"type": "MultiPolygon",
			"coordinates": [geometry_dict.get("coordinates")],
		}
	elif geom_type != "MultiPolygon":
		raise InvalidGeometryError(f"Unsupported geometry type: {geom_type}")
	return from_shape(shape(geometry_dict), srid=4326)


def extract_coordinates(wkb_element):
	"""Extract coordinate arrays from a stored WKBElement."""
	return mapping(to_shape(wkb_element)).get("coordinates")
