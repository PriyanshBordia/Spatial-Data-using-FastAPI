from http.client import HTTPResponse

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db import crud
from ..db import models
from ..db import schemas
from ..db import sessions
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
        if country is None or len(country) == 0:
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
        response = crud.format_response(data=[country])
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


@app.post("/country/create/")
async def create_country(country: schemas.CountryCreate,
                         db: Session = Depends(get_db)):
    try:
        check_country_in_db = crud.get_country_by_code(db, country.iso_a3)
        if check_country_in_db is None or len(check_country_in_db) == 0:
            crud.insert_country(db, country)
            response = crud.format_response(data=[country])
            return response
        else:
            return HTTPException(status_code=409,
                                 detail="Country already exists.")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@app.put("/country/update/{id}")
async def update_country(id: int,
                         country: schemas.CountryCreate,
                         db: Session = Depends(get_db)):
    try:
        check_country_in_db = crud.get_country_by_id(db, id)
        if check_country_in_db is not None and len(check_country_in_db) == 1:
            message = crud.update_country(db, id, country)
            print(message)
            response = crud.format_response(data=[country], message=message)
            return response
        else:
            return HTTPException(status_code=404,
                                 detail="Country does not exist.")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@app.delete("/country/delete/{id}")
async def delete_country(id: int, db: Session = Depends(get_db)):
    try:
        country = crud.get_country_by_id(db, id)
        if country is not None and len(country) == 1:
            message = crud.delete_country(db, country)
            response = crud.format_response(data=[country], message=message)
            return response
        else:
            return HTTPException(status_code=404,
                                 detail="Country does not exist.")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
