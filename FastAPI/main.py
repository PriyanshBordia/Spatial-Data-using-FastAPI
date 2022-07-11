from config import settings
from db.sessions import session
from fastapi import FastAPI
from db.schemas import Country

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/")
async def home():
    return {"message": "API is fast.."}


@app.get("/countries")
async def get_all_countries():
    countries = Country()
    return {"countries": countries}
