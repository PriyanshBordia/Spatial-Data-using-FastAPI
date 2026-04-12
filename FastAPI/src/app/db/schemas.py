from pydantic import BaseModel, ConfigDict

from ..core.geometry import extract_coordinates


class CountryBase(BaseModel):
	admin: str
	iso_a3: str
	geom: dict


class Country(CountryBase):
	id: int
	model_config = ConfigDict(from_attributes=True)


class CountryCreate(CountryBase):
	pass


class CountryResponse(BaseModel):
	id: int
	name: str
	code: str
	coordinates: object

	@classmethod
	def from_orm_model(cls, country) -> "CountryResponse":
		coords = extract_coordinates(country.geom)
		return cls(id=country.id, name=country.admin, code=country.iso_a3, coordinates=coords)
