from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from ..core.dependencies import get_db, verify_api_key
from ..core.exceptions import DuplicateError, InvalidGeometryError, NotFoundError
from ..db import schemas
from ..services import country as country_service

router = APIRouter()


def _serialize(country) -> dict:
	return schemas.CountryResponse.from_orm_model(country).model_dump()


def ok(data, message="API is fast..") -> dict:
	items = [_serialize(c) for c in data] if isinstance(data, list) else [_serialize(data)]
	return {"success": True, "message": message, "meta": {"size": len(items)}, "result": items}


def ok_raw(items: list[dict], message="API is fast..") -> dict:
	return {"success": True, "message": message, "meta": {"size": len(items)}, "result": items}


def err(messages: list[str]) -> dict:
	return {"success": False, "error": {"message": messages}}


@router.get("/")
async def home():
	return ok_raw([], "API is fast..")


@router.get("/populate_data")
async def populate_data_endpoint(db: Session = Depends(get_db)):
	try:
		country_service.populate_from_geojson(db, "app/data/countries.geojson")
		return ok_raw([])
	except Exception:
		return err(["Failed to populate data. The database may already contain country records."])


@router.get("/country/id/{id}")
async def get_country_id(id: int, db: Session = Depends(get_db)):
	try:
		return ok(country_service.get_by_id(db, id))
	except NotFoundError as e:
		return err([str(e)])


@router.get("/country/code/{code}")
async def get_country_code(code: str, db: Session = Depends(get_db)):
	try:
		return ok(country_service.get_by_code(db, code))
	except NotFoundError as e:
		return err([str(e)])


@router.get("/country/name/{name}")
async def get_country_name(name: str, db: Session = Depends(get_db)):
	try:
		return ok(country_service.get_by_name(db, name))
	except NotFoundError as e:
		return err([str(e)])


@router.get("/country/name/contains/{name}")
async def get_country_name_contains(name: str, db: Session = Depends(get_db)):
	try:
		return ok(country_service.search_by_name(db, name))
	except NotFoundError as e:
		return err([str(e)])


@router.get("/countries")
async def get_all_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	countries = country_service.get_all(db, skip=skip, limit=limit)
	return ok(countries)


@router.post("/country/create/", dependencies=[Depends(verify_api_key)])
async def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
	try:
		created = country_service.create(db, country)
		return ok(created, "Country inserted successfully.")
	except (DuplicateError, InvalidGeometryError) as e:
		return err([str(e)])


@router.put("/country/update/{id}", dependencies=[Depends(verify_api_key)])
async def update_country(id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)):
	try:
		updated = country_service.update(db, id, country)
		return ok(updated, "Country updated successfully.")
	except (NotFoundError, DuplicateError, InvalidGeometryError) as e:
		return err([str(e)])


@router.delete("/country/delete/{id}", dependencies=[Depends(verify_api_key)])
async def delete_country(id: int, db: Session = Depends(get_db)):
	try:
		deleted = country_service.delete(db, id)
		return ok(deleted, "Country deleted successfully.")
	except NotFoundError as e:
		return err([str(e)])


@router.get("/country/neighbors/{id}")
async def get_neighbors(id: int, db: Session = Depends(get_db)):
	try:
		neighbors, message = country_service.get_neighbors(db, id)
		return ok(neighbors, message)
	except NotFoundError as e:
		return err([str(e)])
