from sqlalchemy.orm import Session

from ..utils.utility import error_response, format_country, normalize_geometry, success_response
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
			return success_response(data=[format_country(country)])
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
			return success_response(data=[format_country(country)])
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
			return success_response(data=[format_country(country)])
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
			countries = [format_country(country) for country in countries]
			return success_response(data=countries)
		else:
			return error_response(error=[(f"No country contains `{name}` in name.")])
	except Exception as e:
		return error_response(error=[str(e)])


def get_all_countries(db: Session, skip: int = 0, limit: int = 100) -> dict:
	"""
		SELECT *
		FROM countries_country
		OFFSET skip LIMIT limit
	"""
	try:
		countries = db.query(models.Country).offset(skip).limit(limit).all()
		countries = [format_country(country) for country in countries]
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
			wkb_element = normalize_geometry(country.geom)
			if wkb_element is None:
				return error_response(error=["Incorrect input field geom.!"])
			db_country = models.Country(admin=country.admin, iso_a3=country.iso_a3, geom=wkb_element)
			db.add(db_country)
			db.commit()
			db.refresh(db_country)
			return success_response(data=[format_country(db_country)], message="Country inserted successfully.")
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
		existing = db.query(models.Country).filter(models.Country.id == id).one_or_none()
		if existing is not None:
			duplicate = db.query(models.Country).filter(
				models.Country.id != id,
				(models.Country.iso_a3 == country.iso_a3) | (models.Country.admin == country.admin)
			).one_or_none()
			if duplicate is None:
				wkb_element = normalize_geometry(country.geom)
				if wkb_element is None:
					return error_response(error=["Incorrect input field geom.!"])
				existing.admin = country.admin
				existing.iso_a3 = country.iso_a3
				existing.geom = wkb_element
				db.commit()
				db.refresh(existing)
				return success_response(data=[format_country(existing)], message="Country updated successfully.")
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
			country_data = format_country(country)
			db.delete(country)
			db.commit()
			return success_response(data=[country_data], message="Country deleted successfully.")
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
				neighbors = [format_country(c) for c in neighbors]
				return success_response(data=neighbors, message="Neighbors found.")
			else:
				return success_response(data=[], message="Neighbors not found.")
		else:
			return error_response(error=[(f"Country with id: {id} does not exists.!")])
	except Exception as e:
		return error_response(error=[str(e)])
