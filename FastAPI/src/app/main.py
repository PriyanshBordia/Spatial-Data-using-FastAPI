from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

from ..db import crud, schemas, sessions
from .config import settings

# models.Base.metadata.create_all(bind=sessions.engine)

# Create FastAPI object
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, contact=settings.CONTACT)


def get_db():
	db = sessions.session()
	try:
		yield db
	finally:
		db.close()


@app.get("/")
async def home():
	try:
		return crud.success_response(data=[])
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/country/id/{id}")
async def get_country_id(id: int, db: Session = Depends(get_db)):
	try:
		return crud.get_country_by_id(db, id)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/country/code/{code}")
async def get_country_code(code: str, db: Session = Depends(get_db)):
	try:
		return crud.get_country_by_code(db, code)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/country/name/contains/{name}")
async def get_country_name(name: str, db: Session = Depends(get_db)):
	try:
		return crud.get_country_by_name_contains(db, name)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/country/name/{name}")
async def get_country_name(name: str, db: Session = Depends(get_db)):
	try:
		return crud.get_country_by_name(db, name)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/countries")
async def get_all_countries(db: Session = Depends(get_db)):
	try:
		return crud.get_all_countries(db)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.post("/country/create/")
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
	try:
		return crud.insert_country(db, country)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.put("/country/update/{id}")
async def update_country(id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)):
	try:
		return crud.update_country(db, id, country)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.delete("/country/delete/{id}")
async def delete_country(id: int, db: Session = Depends(get_db)):
	try:
		return crud.delete_country(db, id)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))


@app.get("/country/neighbors/{id}")
async def get_neighbors(id: int, db: Session = Depends(get_db)):
	try:
		return crud.get_neighboring_countries(db, id)
	except Exception as e:
		return HTTPException(status_code=400, detail=str(e))
