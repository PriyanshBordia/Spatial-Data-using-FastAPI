from db import models, schemas
from sqlalchemy.orm import Session


def get_countries(db: Session):
    try:
        return db.query(models.Country).all()
    except Exception as e:
        raise e


def get_country_by_admin(db: Session, admin: str):
    try:
        return db.query(models.Country).filter(models.Country.admin == admin).all()
    except Exception as e:
        raise e
