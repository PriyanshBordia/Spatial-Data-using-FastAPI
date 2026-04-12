from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from ..config import settings
from ..db.engine import session

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
	if settings.API_KEY and api_key != settings.API_KEY:
		raise HTTPException(status_code=403, detail="Invalid or missing API key")


def get_db():
	db = session()
	try:
		yield db
	finally:
		db.close()
