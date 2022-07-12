from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from config import settings
from db import models, schemas, sessions, crud

models.Base.metadata.create_all(bind=sessions.engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

def get_db():
	db = sessions.session()
	try:
		yield db
	finally:
		db.close()


@app.get("/")
async def home():
	return {"message": "API is fast.."}


@app.get("/country/{admin}", response_model=schemas.Country)
async def get_all_countries(admin: str, db: Session = Depends(get_db)):
	country = crud.get_country_by_admin(db, admin)
	if country is None:
		return HTTPException(status_code=404, detail="Country not Found.")
	return country
