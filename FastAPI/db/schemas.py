from pydantic import BaseModel


class Country(BaseModel):
    id: int
    admin: str
    iso_a3: str
    geom: list

    class Config:
        orm_mode = True
