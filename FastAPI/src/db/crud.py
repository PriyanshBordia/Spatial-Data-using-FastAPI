from django.contrib.gis.geos import MultiPolygon, Polygon
from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def success_response(data: list, message="API is fast..") -> dict:
	try:
		response = {"message": "", "meta": {"size": 0}, "result": [], "success": True}
		response["message"] = message
		response["meta"]["size"] = len(data)
		response["result"].extend(data)
	except Exception as e:
		raise e


def error_response(error: list) -> dict:
	try:	
		response = {"error": {"code": []}, "success": False}
		response["error"]["code"].extend(error)
		return response
	except Exception as e:
		raise e


def check_country(db: Session, code: str) -> bool:
	try:
		return db.query(models.Country).filter(models.Country.iso_a3 == code).exists()
	except Exception as e:
		raise e


def get_country_by_id(db: Session, id: int) -> dict:
	"""
		SELECT *
		FROM countries_country 
		WHERE id = id
	"""
	try:
		country = db.query(models.Country).filter(models.Country.id == id).one()
		if country is not None:
			return success_response(data=[country])
		else:
			return error_response(error=["Country does not exist."])
	except Exception as e:
		raise e


def get_country_by_code(db: Session, code: str) -> dict:
	"""
		SELECT * 
		FROM countries_country 
		WHERE iso_a3 = code
	"""
	try:
		country = db.query(models.Country).filter(models.Country.iso_a3 == code).one()
		if country is not None:
			return success_response(data=[country])
		else:
			return error_response(error=["Country does not exist."])
	except Exception as e:
		raise e


def get_country_by_name(db: Session, name: str) -> dict:
	"""
		SELECT * 
		FROM countries_country 
		WHERE admin = name
	"""
	try:
		country = db.query(models.Country).filter(models.Country.admin == name).one()
		if country is not None:
			return success_response(data=[country])
		else:
			return error_response(error=["Country does not exist."])
	except Exception as e:
		raise e


def get_all_countries(db: Session) -> dict:
	"""
		SELECT * 
		FROM countries_country
	"""
	try:
		countries = db.query(models.Country).with_entities(models.Country.id, models.Country.admin, models.Country.iso_a3).all()
		return success_response(data=countries)
	except Exception as e:
		raise e


def insert_country(db: Session, country: schemas.CountryCreate) -> dict:
	"""
		INSERT INTO countries_country(id, admin, iso_a3, geom)
		VALUES (country.admin, country.iso_a3, country.geom)
	"""
	try:
		if not check_country(db, country.code):
			db.add(models.Country(**country.dict()))
			db.commit()
			db.refresh(country)
			return success_response(data=[country], message="Country inserted successfully.")
		else:
			return error_response(error=["Country already exists.!"])
	except Exception as e:
		raise e
	

def update_country(db: Session, id: int, country: schemas.CountryCreate) -> dict:
	"""
		UPDATE countries_country 
		SET admin = admin, iso_a3 = iso_a3 
		WHERE id = id
	"""
	try:
		if check_country(db, country.code):
			db.query(models.Country).filter(models.Country.id == id).update(country.__dict__)
			db.commit()
			return success_response(data=[country], message=(f"Country with id: {id} updated successfully."))
		else:
			return error_response(error=["Country does not exists.!"])
	except Exception as e:
		raise e


def delete_country(db: Session, id: int) -> dict:
	"""
		DELETE 
		FROM countries_country
		WHERE id = country.id
	"""
	try:
		country = db.query(models.Country).filter(models.Country.id == id).all()
		if len(country) > 0:
			db.delete(country)
			db.commit()
			return success_response(data=[country], message=(f"Country with id: {id} deleted successfully."))
		else:
			return error_response(error=["Country does not exists.!"])
	except Exception as e:
		raise e


def get_neighboring_countries(db: Session, country: schemas.Country) -> dict:
	"""
	"""
	try:
		# TODO
		raise NotImplementedError
	except Exception as e:
		raise e