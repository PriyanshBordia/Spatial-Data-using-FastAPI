from pydantic import BaseModel, ConfigDict


class CountryBase(BaseModel):
	admin: str
	iso_a3: str
	geom: dict


class Country(CountryBase):
	id: int
	model_config = ConfigDict(from_attributes=True)


class CountryCreate(CountryBase):
	pass
