from fastapi import FastAPI

from models import Country

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "API is fast.."}


@app.get("/countries")
async def get_country_cord(countries: list[Country]):
    return countries
