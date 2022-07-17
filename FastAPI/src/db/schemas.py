from pydantic import BaseModel
from shapely.geometry import MultiPolygon


class CountryBase(BaseModel):
	admin: str
	iso_a3: str


class Country(CountryBase):
	id: int
	geom: str

	class Config:
		orm_mode = True


class CountryCreate(CountryBase):
	pass
