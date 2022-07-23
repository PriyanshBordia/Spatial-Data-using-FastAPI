from django.contrib.gis.geos import GEOSGeometry
from sqlalchemy.orm import Session

from utils.utility import *
from . import models, schemas


def get_country_by_id(db: Session, id: int) -> dict:
	"""
		SELECT *
		FROM countries_country 
		WHERE id = id
	"""
	try:
		country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
		if country is not None:
			return success_response(data=[format(country)])
		else:
			return error_response(error=[(f"Country with id: {id} does not exist.")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_country_by_code(db: Session, code: str) -> dict:
	"""
		SELECT * 
		FROM countries_country 
		WHERE iso_a3 = code
	"""
	try:
		country = db.query(models.Country).filter(models.Country.iso_a3 == code.upper()).one_or_none()
		if country is not None:
			return success_response(data=[format(country)])
		else:
			return error_response(error=[(f"Country with code: {code} does not exist.")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_country_by_name(db: Session, name: str) -> dict:
	"""
		SELECT * 
		FROM countries_country 
		WHERE admin = name
	"""
	try:
		country = db.query(models.Country).filter(models.Country.admin == name).one_or_none()
		if country is not None:
			return success_response(data=[format(country)])
		else:
			return error_response(error=[(f"Country with name: {name} does not exist.")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_country_by_name_contains(db: Session, name: str) -> dict:
	"""
		SELECT * 
		FROM countries_country 
		WHERE admin like "%name%"
	"""
	try:
		countries = db.query(models.Country).filter(models.Country.admin.contains(name)).all()
		if len(countries) > 0:
			countries = [format(country) for country in countries]
			return success_response(data=countries)
		else:
			return error_response(error=[(f"No country contains `{name}` in name.")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_all_countries(db: Session) -> dict:
	"""
		SELECT * 
		FROM countries_country
	"""
	try:
		countries = db.query(models.Country).all()
		countries = [format(country) for country in countries]
		return success_response(data=countries)
	except Exception as e:
		return error_response(error=[str(e)])


def insert_country(db: Session, country: schemas.CountryCreate) -> dict:
	"""
		INSERT INTO countries_country(id, admin, iso_a3, geom)
		VALUES (country.admin, country.iso_a3, country.geom)
	"""
	try:
		if db.query(models.Country).filter(models.Country.iso_a3 == country.iso_a3).one_or_none() is None and db.query(models.Country).filter(models.Country.admin == country.admin).one_or_none() is None:
			geometry = country.geom
			if geometry.get("type") == "Polygon":
				geometry["type"] = "MultiPolygon"
				geometry["coordinates"] = [geometry.get("coordinates")]
			elif geometry.get("type") == "MultiPolygon":
				geometry["coordinates"] = geometry.get("coordinates")
			else:
				return error_response(error=["Incorrect input field geom.!"])
			country.geom = (GEOSGeometry(geojson.dumps(geometry)).hexewkb).decode()
			db.add(models.Country(**country.dict()))
			db.commit()
			country = db.query(models.Country).filter(models.Country.iso_a3 == country.iso_a3).one_or_none()
			return success_response(data=[format(country)], message="Country inserted successfully.")
		else:
			return error_response(error=["Country already exists.!"])
	except Exception as e:
		return error_response(error=[str(e)])
	

def update_country(db: Session, id: int, country: schemas.CountryCreate) -> dict:
	"""
		UPDATE countries_country 
		SET admin = admin, iso_a3 = iso_a3 
		WHERE id = id
	"""
	try:
		if db.query(models.Country).filter(models.Country.id == id) is not None:
			if db.query(models.Country).filter(models.Country.iso_a3 == country.iso_a3).one_or_none() is None and db.query(models.Country).filter(models.Country.admin == country.admin).one_or_none() is None:
				geometry = country.geom
				if geometry.get("type") == "Polygon":
					geometry["type"] = "MultiPolygon"
					geometry["coordinates"] = [geometry.get("coordinates")]
				elif geometry.get("type") == "MultiPolygon":
					geometry["coordinates"] = geometry.get("coordinates")
				else:
					return error_response(error=["Incorrect input field geom.!"])
				country.geom = (GEOSGeometry(geojson.dumps(geometry)).hexewkb).decode()
				db.query(models.Country).filter(models.Country.id == id).update(country.dict())
				db.commit()
				country = db.query(models.Country).filter(models.Country.id == id).one_or_none() 
				return success_response(data=[format(country)], message="Country updated successfully.")
			else:
				return error_response(error=[(f"Country with name: {country.admin} and code: {country.iso_a3} already exists.!")])
		else:
			return error_response(error=[(f"Country with id: {id} does not exists.!")])
	except Exception as e:
		return error_response(error=[str(e)])


def delete_country(db: Session, id: int) -> dict:
	"""
		DELETE 
		FROM countries_country
		WHERE id = country.id
	"""
	try:
		country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
		if country is not None:
			db.delete(country)
			db.commit()
			return success_response(data=[format(country)], message="Country deleted successfully.")
		else:
			return error_response(error=[(f"Country with id: {id} does not exists.!")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_neighboring_countries(db: Session, id: int) -> dict:
	"""
		SELECT id, admin, iso_a3, ST_AsText(geom)
		FROM countries_country
		HAVING ST_Distance(country.geom)
	"""
	try:
		country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
		if country is not None:
			neighbors = db.query(models.Country).filter(models.Country.id != id, models.Country.geom.intersects(country.geom)).all()
			if len(neighbors) > 0:
				neighbors = [format(country) for country in neighbors]
				return success_response(data=neighbors, message="Neighbors found.")
			else:
				return success_response(data=[], message="Neighbors not found.")
		else:
			return error_response(error=[(f"Country with id: {id} does not exists.!")])
	except Exception as e:
		return error_response(error=[str(e)])