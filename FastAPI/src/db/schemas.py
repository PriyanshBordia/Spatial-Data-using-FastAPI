from pydantic import BaseModel


class CountryBase(BaseModel):
    id: int
    admin: str
    iso_a3: str
    geom: str


class Country(CountryBase):
    id: int
    admin: str
    iso_a3: str
    geom: str

    class Config:
        orm_mode = True


class CountryCreate(CountryBase):
    admin: str
    iso_a3: str
    geom: str
