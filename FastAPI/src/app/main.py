from fastapi import FastAPI

from .config import settings
from .db.engine import Base, engine
from .routes import api, web

Base.metadata.create_all(bind=engine)

app = FastAPI(
	title=settings.PROJECT_NAME,
	version=settings.PROJECT_VERSION,
	contact=settings.CONTACT,
)

app.include_router(api.router)
app.include_router(web.router)
