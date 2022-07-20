from geoalchemy2.functions import ST_AsGeoJSON
from sqlalchemy.orm import Session

from ..utils.utility import *
from . import models, schemas


def check_country(db: Session, id=None, code=None) -> bool:
    try:
        if id is not None:
            country = db.query(models.Country).filter(
                models.Country.id == id).one_or_none()
        elif code is not None:
            country = db.query(models.Country).filter(
                models.Country.iso_a3 == code).one_or_none()
        return country is not None
    except Exception as e:
        return error_response(error=[str(e)])


def get_country_by_id(db: Session, id: int) -> dict:
    """
            SELECT *
            FROM countries_country 
            WHERE id = id
    """
    try:
        country = db.query(models.Country.id, models.Country.admin, models.Country.iso_a3,
                           models.Country.geom.ST_AsGeoJSON()).filter(models.Country.id == id).one_or_none()
        if country is not None:
            return success_response(data=[format(country)])
        else:
            return error_response(error=[(f"Country with id: {id} does not exist.")])
    except Exception as e:
        print(e)
        return error_response(error=[str(e)])


def get_country_by_code(db: Session, code: str) -> dict:
    """
            SELECT * 
            FROM countries_country 
            WHERE iso_a3 = code
    """
    try:
        country = db.query(models.Country.id, models.Country.admin, models.Country.iso_a3,
                           models.Country.geom.ST_AsGeoJSON()).filter(models.Country.iso_a3 == code.upper()).one_or_none()
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
        country = db.query(models.Country.id, models.Country.admin, models.Country.iso_a3,
                           models.Country.geom.ST_AsGeoJSON()).filter(models.Country.admin == name).one_or_none()
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
        countries = db.query(models.Country).filter(models.Country.admin.contains(
            name)).with_entities(models.Country.id, models.Country.admin, models.Country.iso_a3).all()
        if len(countries) > 0:
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
        countries = db.query(models.Country).with_entities(
            models.Country.id, models.Country.admin, models.Country.iso_a3).all()
        return success_response(data=countries)
    except Exception as e:
        return error_response(error=[str(e)])


def insert_country(db: Session, country: schemas.CountryCreate) -> dict:
    """
            INSERT INTO countries_country(id, admin, iso_a3, geom)
            VALUES (country.admin, country.iso_a3, country.geom)
    """
    try:
        if not check_country(db, code=country.iso_a3):
            db.add(models.Country(**country.dict()))
            db.commit()
            return success_response(data=[country], message="Country inserted successfully.")
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
        if check_country(db, id=id):
            db.query(models.Country).filter(
                models.Country.id == id).update(country.__dict__)
            db.commit()
            return success_response(data=[country], message="Country updated successfully.")
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
        country = db.query(models.Country).filter(
            models.Country.id == id).one_or_none()
        if country is not None:
            db.delete(country)
            db.commit()
            return success_response(data=[country], message="Country deleted successfully.")
        else:
            return error_response(error=[(f"Country with id: {id} does not exists.!")])
    except Exception as e:
        return error_response(error=[str(e)])

##


def get_neighboring_countries(db: Session, id: int) -> dict:
    """
            SELECT id, admin, iso_a3, ST_AsText(geom)
            FROM countries_country
            HAVING ST_Distance(country.geom)
    """
    try:
        country = db.query(models.Country).filter(
            models.Country.id == id).one_or_none()
        if country is not None:
            neighbors = db.query(models.Country).filter(models.Country.id != id, models.Country.geom.intersects(
                country.geom)).with_entities(models.Country.id, models.Country.admin, models.Country.iso_a3).all()
            if len(neighbors) > 0:
                return success_response(data=neighbors, message="Neighbors found.")
            else:
                return success_response(data=[], message="Neighbors not found.")
        else:
            return error_response(error=[(f"Country with id: {id} does not exists.!")])
    except Exception as e:
        return error_response(error=[str(e)])
