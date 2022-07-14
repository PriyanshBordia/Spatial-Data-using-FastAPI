from curses.ascii import HT

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from termcolor import cprint

from ..db import crud, models, schemas, sessions
from .config import settings

# models.Base.metadata.create_all(bind=sessions.engine)

# Create FastAPI object
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


def get_db():
    db = sessions.session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    response = crud.format_response()
    return response


@app.get("/countries")
async def get_all_countries(db: Session = Depends(get_db)):
    try:
        countries = crud.get_countries(db)
        if countries is None:
            return HTTPException(status_code=404, detail="Not Found.")
        elif len(countries) == 0:
            return HTTPException(status_code=401, detail="Unauthorized.")
        response = crud.format_response(data=countries)
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/country/id/{id}")
async def get_country_id(id: int, db: Session = Depends(get_db)):
    try:
        country = crud.get_country_by_id(db, id)
        if country is None:
            return HTTPException(status_code=404, detail="Country not Found.")
        response = crud.format_response(data=country)
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/country/code/{code}")
async def get_country_code(code: str, db: Session = Depends(get_db)):
    try:
        country = crud.get_country_by_code(db, code)
        if country is None or len(country) == 0:
            return HTTPException(status_code=404, detail="Country not Found.")
        response = crud.format_response(data=country)
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/country/name/{name}")
async def get_country_name(name: str, db: Session = Depends(get_db)):
    try:
        country = crud.get_country_by_name(db, name)
        if country is None or len(country) == 0:
            return HTTPException(status_code=404, detail="Country not Found.")
        response = crud.format_response(data=country)
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
