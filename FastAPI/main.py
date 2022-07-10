from config import settings
from db.sessions import session
from fastapi import FastAPI
from pydantic import BaseModel


class Country(BaseModel):
    ogc_fid: int
    admin: str
    iso_a3: str
    geom: list


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/")
async def home():
    return {"message": "API is fast.."}


@app.get("/countries")
async def get_all_countries():
    countries = Country.objects.all()
    return {"countries": countries}
