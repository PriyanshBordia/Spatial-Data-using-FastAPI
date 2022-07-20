from geojson import MultiPolygon
from pydantic import BaseModel


class CountryBase(BaseModel):
    admin: str
    iso_a3: str
    geom: MultiPolygon


class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True


class CountryCreate(CountryBase):
    pass
