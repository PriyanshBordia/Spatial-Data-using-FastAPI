from django.contrib.gis.geos import MultiPolygon, Polygon
from sqlalchemy.orm import Session

from . import models, schemas


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
        # ("SELECT * FROM countries_country WHERE id = :id", {"id": id}).fetchall()
        return db.query(models.Country).filter(models.Country.id == id).all()
    except Exception as e:
        raise e


def get_country_by_code(db: Session, code: str):
    try:
        # ("SELECT * FROM countries_country WHERE iso_a3 = :code", {"code": code}).fetchall()
        return db.query(models.Country).filter(models.Country.iso_a3 == code).all()
    except Exception as e:
        raise e


def get_country_by_name(db: Session, name: str):
    try:
        # ("SELECT * FROM countries_country WHERE admin = :name", {"name": name}).fetchall()
        return db.query(models.Country).filter(models.Country.admin == name).all()
    except Exception as e:
        raise e


def get_neighboring_countries(db: Session, country: schemas.Country):
    # TODO
    raise NotImplementedError


def get_countries(db: Session):
    try:
        # ("SELECT * FROM countries_country").fetchall()
        return (
            db.query(models.Country)
            .with_entities(
                models.Country.id, models.Country.admin, models.Country.iso_a3
            )
            .all()
        )
    except Exception as e:
        raise e


def insert_country(db: Session, country: schemas.CountryCreate):
    try:
        print(country.dict())
        db.add(models.Country(**country.dict()))
        db.commit()
        db.refresh(country)
    except Exception as e:
        raise e


def update_country(db: Session, id: int, country: schemas.CountryCreate):
    try:
        # ("UPDATE countries_country SET admin = :admin, iso_a3 = :iso_a3 WHERE id :id;", {"admin": country.admin, "iso_a3": country.iso_a3, "id": id})
        db.query(models.Country).filter(models.Country.id == id).update(
            country.__dict__
        )
        db.commit()
        return f"Country with id: {id} updated successfully."
    except Exception as e:
        raise e


def delete_country(db: Session, country: schemas.Country):
    try:
        db.delete(country)
        db.commit()
        return f"Country with id: {id} deleted successfully."
    except Exception as e:
        raise e


"""
{
    "geom": "0106000020E6100000010000000103000000010000001A000000362D7CD3CD7F51C098543BD7B8272940382D7CD3ED7B51C06810942C3E102940382D7CD32D7B51C0408D3ED7D8092940ACF97BD39B7A51C0707A3DD778FE2840705AD128557851C020A03FD738E82840A8B67CD31D7851C0181DEA81D3DA28406889277ED67851C0408D3ED7D8D5284004D97CD3297A51C030DE3BD7E8D52840342D7CD38D7B51C078673CD718DA28409E28D2287D7C51C0787A3DD778E12840382D7CD32D7B51C0787A3DD778E12840382D7CD32D7B51C0D0C541D7F8E428408AC1D128597D51C0704F42D728ED2840E6E3D128C58151C0005C982CBE0B2940623E7CD3138351C0B055ED81F30F294076A57CD3B78351C0C8163FD708132940AC44277EFE8351C0E8C541D7F8172940A028D228DD8351C0784F42D7281D2940E4E3D128458351C018DE3BD7E8252940B044277E1E8351C078FD922CDE2A2940B044277E5E8351C0E02FEB81333329404206D228D18351C0A8EA912C7E3A2940FE4AD228E98351C0E82FEB8133402940B044277E1E8351C0F0033ED7A8432940725AD128758051C0903C41D7C82B2940362D7CD3CD7F51C098543BD7B8272940",
    "admin": "Atlantis",
    "iso_a3": "ATL"
}
"""
