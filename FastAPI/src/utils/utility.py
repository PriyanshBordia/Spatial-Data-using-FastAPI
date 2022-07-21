import geojson

from ..db import crud, models


def format(country: tuple) -> dict:
	try:
		return {"id": country[0], "name": country[1], "code": country[2], "coordinates": geojson.loads(country[3]).get("coordinates")}
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
		response = {"error": {"code": []}, "success": False}
		response["error"]["code"].extend(error)
		return response
	except Exception as e:
		raise e


def get_boundary_points(country: models.Country):
	try:
		boundary_points = []
		for polygon in country:
			for line in polygon:
				for point in line:
					boundary_points.append(point)
		return boundary_points
	except Exception as e:
		raise e


def get_all_neighbors(boundary_points: list) -> list:
	try:
		response = crud.get_all_countries()
	except Exception as e:
		raise e
