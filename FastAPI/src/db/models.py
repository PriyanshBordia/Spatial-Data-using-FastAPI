from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .sessions import Base


class Country(Base):
    __tablename__ = "countries_country"

    id = Column(Integer, primary_key=True)
    admin = Column(String, unique=True)
    iso_a3 = Column(String, unique=True)
    geom = Column(String)
