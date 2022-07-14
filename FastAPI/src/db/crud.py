from . import models, schemas
from sqlalchemy.orm import Session


def template() -> dict:
    return {"message": "", "meta": {"size": 0}, "result": [], "success": False}


def format_response(data=list(), message="API is fast..") -> dict:
    response = template()
    response["message"] = message
    response["result"].extend(data)
    response["meta"]["size"] = len(data)
    response["success"] = True
    return response


def get_country_by_id(db: Session, id: int):
    try:
        # return db.execute("SELECT * FROM countries_country WHERE id = :id", {"id": id}).fetchall()
        return db.query(models.Country).filter(models.Country.id == id).all()
    except Exception as e:
        raise e


def get_country_by_code(db: Session, code: str):
    try:
        # return db.execute("SELECT * FROM countries_country WHERE iso_a3 = :code", {"code": code}).fetchall()
        return db.query(models.Country).filter(models.Country.iso_a3 == code).all()
    except Exception as e:
        raise e


def get_country_by_name(db: Session, name: str):
    try:
        # return db.execute("SELECT * FROM countries_country WHERE admin = :name", {"name": name}).fetchall()
        return db.query(models.Country).filter(models.Country.admin == name).all()
    except Exception as e:
        raise e


def get_neighboring_countries(db: Session, country: schemas.Country):
    # TODO
    raise NotImplementedError


def get_countries(db: Session):
    try:
        # return db.execute("SELECT * FROM countries_country").fetchall()
        return (
            db.query(models.Country)
            .with_entities(
                models.Country.id, models.Country.admin, models.Country.iso_a3
            )
            .all()
        )
    except Exception as e:
        raise e


def insert_country(db: Session, country: schemas.Country):
    # TODO
    raise NotImplementedError
    # try:
    # except Exception as e:
    # print(e)


def delete_country_by_id(db: Session, id: int):
    # TODO
    raise NotImplementedError
