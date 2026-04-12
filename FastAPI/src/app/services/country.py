import geojson
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
from shapely.geometry import shape
from sqlalchemy.orm import Session

from ..core.exceptions import DuplicateError, NotFoundError
from ..core.geometry import to_wkb_multipolygon
from ..db import models, schemas


def get_by_id(db: Session, id: int) -> models.Country:
	country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
	if country is None:
		raise NotFoundError("Country", f"id: {id}")
	return country


def get_by_code(db: Session, code: str) -> models.Country:
	country = db.query(models.Country).filter(models.Country.iso_a3 == code.upper()).one_or_none()
	if country is None:
		raise NotFoundError("Country", f"code: {code}")
	return country


def get_by_name(db: Session, name: str) -> models.Country:
	country = db.query(models.Country).filter(models.Country.admin == name).one_or_none()
	if country is None:
		raise NotFoundError("Country", f"name: {name}")
	return country


def search_by_name(db: Session, fragment: str) -> list[models.Country]:
	countries = db.query(models.Country).filter(models.Country.admin.contains(fragment)).all()
	if not countries:
		raise NotFoundError("Country", f"name containing '{fragment}'")
	return countries


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[models.Country]:
	return db.query(models.Country).offset(skip).limit(limit).all()


def create(db: Session, data: schemas.CountryCreate) -> models.Country:
	if (
		db.query(models.Country).filter(models.Country.iso_a3 == data.iso_a3).one_or_none() is not None
		or db.query(models.Country).filter(models.Country.admin == data.admin).one_or_none() is not None
	):
		raise DuplicateError("Country")
	wkb = to_wkb_multipolygon(data.geom)
	country = models.Country(admin=data.admin, iso_a3=data.iso_a3, geom=wkb)
	db.add(country)
	db.commit()
	db.refresh(country)
	return country


def update(db: Session, id: int, data: schemas.CountryCreate) -> models.Country:
	existing = db.query(models.Country).filter(models.Country.id == id).one_or_none()
	if existing is None:
		raise NotFoundError("Country", f"id: {id}")
	duplicate = (
		db.query(models.Country)
		.filter(
			models.Country.id != id,
			(models.Country.iso_a3 == data.iso_a3) | (models.Country.admin == data.admin),
		)
		.one_or_none()
	)
	if duplicate is not None:
		raise DuplicateError("Country", f"name: {data.admin} and code: {data.iso_a3}")
	wkb = to_wkb_multipolygon(data.geom)
	existing.admin = data.admin
	existing.iso_a3 = data.iso_a3
	existing.geom = wkb
	db.commit()
	db.refresh(existing)
	return existing


def delete(db: Session, id: int) -> models.Country:
	country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
	if country is None:
		raise NotFoundError("Country", f"id: {id}")
	# Detach a snapshot before deletion so the route layer can serialize it
	snapshot = models.Country(id=country.id, admin=country.admin, iso_a3=country.iso_a3, geom=country.geom)
	db.delete(country)
	db.commit()
	return snapshot


def get_neighbors(db: Session, id: int) -> tuple[list[models.Country], str]:
	country = db.query(models.Country).filter(models.Country.id == id).one_or_none()
	if country is None:
		raise NotFoundError("Country", f"id: {id}")
	neighbors = (
		db.query(models.Country)
		.filter(
			models.Country.id != id,
			models.Country.geom.intersects(country.geom),
		)
		.all()
	)
	message = "Neighbors found." if neighbors else "Neighbors not found."
	return neighbors, message


def populate_from_features(db: Session, features: list[dict]) -> int:
	"""Bulk-insert countries from GeoJSON features, skipping duplicates."""
	seen_codes = set()
	seen_names = set()
	existing_codes = {r[0] for r in db.query(models.Country.iso_a3).all()}
	existing_names = {r[0] for r in db.query(models.Country.admin).all()}
	count = 0
	for row in features:
		properties = row.get("properties", {})
		geometry = row.get("geometry")
		admin = properties.get("ADMIN")
		iso_a3 = properties.get("ISO_A3")
		if not admin or not iso_a3 or not geometry:
			continue
		if iso_a3 in existing_codes or iso_a3 in seen_codes:
			continue
		if admin in existing_names or admin in seen_names:
			continue
		seen_codes.add(iso_a3)
		seen_names.add(admin)
		geom_shape = shape(geometry)
		if geom_shape.geom_type == "Polygon":
			geom_shape = ShapelyMultiPolygon([geom_shape])
		wkb = from_shape(geom_shape, srid=4326)
		db.add(models.Country(admin=admin, iso_a3=iso_a3, geom=wkb))
		count += 1
	db.commit()
	return count


def populate_from_geojson(db: Session, path: str) -> int:
	"""Load countries from a GeoJSON file on disk."""
	with open(path) as f:
		features = geojson.load(f)["features"]
	return populate_from_features(db, features)
