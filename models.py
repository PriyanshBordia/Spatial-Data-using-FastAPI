from pydantic import BaseModel

class Country(BaseModel):
	ogc_fid: int
	admin: str
	iso_a3: str
	geom: str
