import pytest
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiPolygon as ShapelyMultiPolygon
from shapely.geometry import Polygon as ShapelyPolygon

from fastapi.testclient import TestClient

from ..config import settings
from ..db import models
from ..db.engine import session
from ..main import app


def make_geom(coords):
	return from_shape(ShapelyMultiPolygon([ShapelyPolygon(coords)]), srid=4326)


# Two adjacent squares (share edge at x=1) and one isolated square
GEOM_A = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
GEOM_B = [(1, 0), (1, 1), (2, 1), (2, 0), (1, 0)]
# Point Nemo area — farthest from any landmass on Earth
GEOM_ISOLATED = [(-130, -48), (-130, -47.99), (-129.99, -47.99), (-129.99, -48), (-130, -48)]


@pytest.fixture()
def db():
	db = session()
	yield db
	db.close()


@pytest.fixture()
def seed_countries(db):
	countries = [
		models.Country(admin="Alphaland", iso_a3="ALP", geom=make_geom(GEOM_A)),
		models.Country(admin="Betaland", iso_a3="BET", geom=make_geom(GEOM_B)),
		models.Country(admin="Gammaland", iso_a3="GAM", geom=make_geom(GEOM_ISOLATED)),
	]
	for c in countries:
		db.add(c)
	db.commit()
	for c in countries:
		db.refresh(c)
	yield countries
	ids = [c.id for c in countries]
	db.query(models.Country).filter(models.Country.id.in_(ids)).delete()
	db.commit()


@pytest.fixture()
def client():
	return TestClient(app)


@pytest.fixture()
def api_key():
	original = settings.API_KEY
	settings.API_KEY = "test-secret-key"
	yield "test-secret-key"
	settings.API_KEY = original
