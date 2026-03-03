from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from .config import settings
from .db import crud, models, schemas, sessions
from .utils.utility import populate_data as _populate_data

models.Base.metadata.create_all(bind=sessions.engine)

# Create FastAPI object
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, contact=settings.CONTACT)

# API Key authentication (S1)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
	if settings.API_KEY and api_key != settings.API_KEY:
		raise HTTPException(status_code=403, detail="Invalid or missing API key")


def get_db():
	db = sessions.session()
	try:
		yield db
	finally:
		db.close()


@app.get("/")
async def home():
	return crud.success_response(data=[])


@app.get("/populate_data")
async def populate_data_endpoint(db: Session = Depends(get_db)):
	try:
		_populate_data(db)
		return crud.success_response(data=[])
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


@app.get("/country/id/{id}")
async def get_country_id(id: int, db: Session = Depends(get_db)):
	return crud.get_country_by_id(db, id)


@app.get("/country/code/{code}")
async def get_country_code(code: str, db: Session = Depends(get_db)):
	return crud.get_country_by_code(db, code)


@app.get("/country/name/{name}")
async def get_country_name(name: str, db: Session = Depends(get_db)):
	return crud.get_country_by_name(db, name)


@app.get("/country/name/contains/{name}")
async def get_country_name_contains(name: str, db: Session = Depends(get_db)):
	return crud.get_country_by_name_contains(db, name)


@app.get("/countries")
async def get_all_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	return crud.get_all_countries(db, skip=skip, limit=limit)


@app.post("/country/create/", dependencies=[Depends(verify_api_key)])
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
	return crud.insert_country(db, country)


@app.put("/country/update/{id}", dependencies=[Depends(verify_api_key)])
async def update_country(id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)):
	return crud.update_country(db, id, country)


@app.delete("/country/delete/{id}", dependencies=[Depends(verify_api_key)])
async def delete_country(id: int, db: Session = Depends(get_db)):
	return crud.delete_country(db, id)


@app.get("/country/neighbors/{id}")
async def get_neighbors(id: int, db: Session = Depends(get_db)):
	return crud.get_neighboring_countries(db, id)
