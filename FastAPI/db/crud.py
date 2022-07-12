from sqlalchemy.orm import Session

from db import models, schemas


def get_country_by_admin(db: Session, admin: str):
	try:
		return db.query(models.Country).filter(models.Country.admin == admin).all()
	except Exception as e:
		raise e